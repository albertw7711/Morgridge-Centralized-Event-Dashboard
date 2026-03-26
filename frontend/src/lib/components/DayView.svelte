<script lang="ts">
	import chevron from '$lib/assets/up-chevron.svg';
	import { buildDayViewEvents, toggleExpandedEvent } from '$lib/features/events/day-view';
	import { calendarSearchQuery, calendarStepMode } from '$lib/stores/calendar-ui';
	import { allEvents } from '$lib/stores/events';
	import { slide } from 'svelte/transition';

	let expandedEventIds: number[] = $state([]);

	let {
		selectedDate = null,
		expandedEventId = null
	}: {
		selectedDate: string | null;
		expandedEventId: number | null;
	} = $props();

	const dayEvents = $derived(buildDayViewEvents($allEvents, selectedDate));

	$effect(() => {
		expandedEventIds = expandedEventId != null ? [expandedEventId] : [];
		void selectedDate;
	});

	function viewDetails(eventId: number): void {
		expandedEventIds = toggleExpandedEvent(expandedEventIds, eventId);
	}

	function isExpanded(eventId: number): boolean {
		return expandedEventIds.includes(eventId);
	}

	function goBackToCalendar(): void {
		calendarStepMode.set('month');
		calendarSearchQuery.set('');
	}
</script>

<div class="w-full">
	<div class="mb-3 flex items-center justify-between gap-2">
		<button
			type="button"
			class="inline-flex items-center gap-1 rounded-lg border border-(--uwGrayLight) bg-(--uwWhite) px-2 py-1 text-sm font-semibold text-(--uwGrayDark) transition-colors hover:bg-(--uwGrayLightest)"
			onclick={goBackToCalendar}
			aria-label="Back to calendar"
		>
			<span aria-hidden="true">←</span>
			<span>Back</span>
		</button>

		{#if selectedDate}
			<p class="text-right text-sm font-medium text-(--uwGrayDark)">
				Showing events for: {selectedDate}
			</p>
		{:else}
			<p class="text-right text-sm text-(--uwGrayDark)/70">
				No date selected. Go back to calendar and choose a day.
			</p>
		{/if}
	</div>

	<div class="dayEvent-container flex flex-col gap-3">
		{#if dayEvents.length > 0}
			{#each dayEvents as event (event.id)}
				<div
					class="event-card w-full rounded-xl border border-(--uwGrayLight) bg-(--uwWhite) p-2 shadow-sm"
				>
					<button
						class="event-header flex h-full w-full items-start justify-between gap-x-3 rounded-xl px-1 py-1 transition-colors hover:bg-(--uwGrayLightest)"
						type="button"
						onclick={() => viewDetails(event.id)}
					>
						<div class="min-w-0 flex-1">
							<h2 class="event-title truncate text-base font-semibold text-(--uwGrayDark)">
								{event.eventTitle}{#if event.food}&nbsp;🍕{/if}
							</h2>
							<p class="mt-0.5 text-sm text-(--uwGrayDark)/75">{event.eventLocation}</p>
							<p class="text-sm font-medium text-(--uwRedDark)">@ {event.eventStartTime}</p>
						</div>
						<span class="toggle mt-0.5 h-6 w-6 text-(--uwGrayDark)">
							<img
								class={`transition-transform duration-300 ease-out ${isExpanded(event.id) ? '' : 'rotate-180'}`}
								src={chevron}
								alt="toggle"
							/>
						</span>
					</button>

					{#if isExpanded(event.id)}
						<div
							class="event-details mt-2 overflow-hidden rounded-lg border border-(--uwGrayLight) bg-(--uwGrayLightest) px-3 py-2"
							transition:slide={{ duration: 360 }}
						>
							<p class="text-xs font-semibold tracking-wide text-(--uwRedDark) uppercase">Host</p>
							<p class="text-sm text-(--uwGrayDark)">{event.eventHost}</p>
							<p class="mt-2 text-xs font-semibold tracking-wide text-(--uwRedDark) uppercase">
								Details
							</p>
							<p class="text-sm text-(--uwGrayDark)">{event.eventDescription}</p>
						</div>
					{/if}
				</div>
			{/each}
		{:else if selectedDate}
			<p class="text-sm text-(--uwGrayDark)/70">No events match this date and search query.</p>
		{/if}
	</div>
</div>
