<script lang="ts">
	import { allEvents } from '$lib/stores/events';
	import { toLocalIsoDate } from '$lib/utils/date';
	import {
		calendarReferenceDate,
		calendarSearchQuery,
		calendarStepMode,
		expandedDayEventId,
		pizzaOnlyFilter
	} from '$lib/stores/calendar-ui';
	import { buildDayViewEvents } from '$lib/features/events/day-view';
	import { getEventSearchMatches } from '$lib/features/events/utils';
	import type { EventInfo } from '$lib/mockEvents';

	let { dayNumber, date }: { dayNumber: number; date: Date } = $props();

	const dateParam = $derived(toLocalIsoDate(date));
	const isToday = $derived(dateParam === toLocalIsoDate(new Date()));
	const dayEvents = $derived(buildDayViewEvents($allEvents, dateParam));
	const normalizedQuery = $derived($calendarSearchQuery.trim().toLowerCase());
	const dayEventMatches = $derived(
		dayEvents.map((event) => ({
			event,
			isMatch: normalizedQuery
				? getEventSearchMatches(event, normalizedQuery, 'preview').length > 0
				: true
		}))
	);

	const MAX_VISIBLE_EVENTS = 3;
	const visibleEvents = $derived(dayEventMatches.slice(0, MAX_VISIBLE_EVENTS));
	const extraEventCount = $derived(dayEvents.length - MAX_VISIBLE_EVENTS);

	// Returns the appropriate highlight class based on pizza filter + search state
	function getEventHighlightClass(event: EventInfo, isMatch: boolean): string {
		const isPizza = $pizzaOnlyFilter && event.food;
		const hasSearch = Boolean(normalizedQuery);

		// Both pizza filter active AND search match
		if (isPizza && hasSearch && isMatch) {
			return 'bg-(--uwRedLight) border-(--uwBlack) text-(--uwBlack)';
		}
		// Pizza filter active (food event)
		if (isPizza) {
			return 'bg-(--uwRedLight) border-(--uwRed) text-(--uwBlack)';
		}
		// Search match only
		if (hasSearch && isMatch) {
			return 'border-(--uwBlack) text-(--uwGrayDark)';
		}
		// Search active but no match — fade out
		if (hasSearch && !isMatch) {
			return 'border-transparent text-(--uwGrayDark)/40';
		}
		// Default
		return 'border-transparent text-(--uwGrayDark)';
	}

	function openDayView(): void {
		calendarReferenceDate.set(new Date(date));
		expandedDayEventId.set(null);
		calendarStepMode.set('day');
	}

	let touchRight = $state(false);
	let touchBottom = $state(false);
	let hoveredEventId = $state<number | -9999>(-9999);

	function mouseHover(e: MouseEvent, id: number) {
		const btn = e.currentTarget as HTMLElement;
		const rect = btn.getBoundingClientRect();
		const tooltipWidth = 288;
		const height = 173;
		const gap = 8;

		const overflowsRight = rect.right + gap + tooltipWidth > window.innerWidth;
		const overflowsLeft = rect.left - gap - tooltipWidth < 0;
		const overflowsBottom = rect.bottom + height > window.innerHeight;

		if (overflowsRight && overflowsLeft) {
			touchRight = false;
		} else if (overflowsRight) {
			touchRight = true;
		} else {
			touchRight = false;
		}

		touchBottom = overflowsBottom;
		hoveredEventId = id;
	}

	function mouseLeave() {
		hoveredEventId = -9999;
	}
</script>

<div
	class="flex h-full w-full flex-col items-stretch justify-start gap-1 overflow-visible rounded border border-transparent transition-colors hover:bg-(--uwGrayLightest)"
>
	<div class="w-full px-1">
		<button type="button" class="block w-full cursor-pointer text-center" onclick={openDayView}>
			{#if isToday}
				<span
					class="inline-flex h-6 w-6 items-center justify-center rounded-full bg-(--uwRed) text-sm font-bold text-white"
				>
					{dayNumber}
				</span>
			{:else}
				{dayNumber}
			{/if}
		</button>
	</div>

	<div class="w-full min-w-0 overflow-visible px-1">
		<div class="flex flex-col gap-1">
			{#each visibleEvents as entry (entry.event.id)}
				<div class="group relative w-full hover:z-[100]">
					<button
						type="button"
						onmouseenter={(e) => mouseHover(e, entry.event.id)}
						onmouseleave={mouseLeave}
						class={`box-border max-h-[250px] w-full cursor-pointer overflow-hidden rounded-lg border px-1 py-0.5 text-left text-[10px] leading-tight transition-colors hover:border-(--uwBlack) hover:bg-(--uwWhite) hover:text-(--uwBlack) ${getEventHighlightClass(entry.event, entry.isMatch)}`}
						onclick={(e) => {
							e.stopPropagation();
							calendarReferenceDate.set(new Date(date));
							expandedDayEventId.set(entry.event.id);
							calendarStepMode.set('day');
						}}
					>
						<span class="event-title block">
							{entry.event.eventTitle}
						</span>

						{#if hoveredEventId === entry.event.id}
							<div
								class={`pointer-events-auto absolute z-50
									${touchRight ? 'right-full pr-2' : 'left-full pl-2'}
									${touchBottom ? 'bottom-0' : 'top-0'}`}
							>
								<div
									class="box-border w-72 rounded-lg border border-gray-200 bg-white p-3 shadow-xl transition-all duration-200"
								>
									<div class="space-y-2">
										<h3 class="text-sm font-bold">
											{entry.event.eventTitle}{#if entry.event.food}&nbsp;🍕{/if}
										</h3>
										<p class="mt-0.5 text-sm text-(--uwGrayDark)/75">{entry.event.eventLocation}</p>
										<p class="text-sm font-medium text-(--uwRedDark)">
											@ {entry.event.eventStartTime}
										</p>
										<p class="text-sm text-(--uwGrayDark)">
											{entry.event.eventDescription?.length > 100
												? entry.event.eventDescription.slice(0, 100) + '...'
												: entry.event.eventDescription}
										</p>
									</div>
								</div>
							</div>
						{/if}
					</button>
				</div>
			{/each}

			{#if extraEventCount > 0}
				<button
					type="button"
					class="cursor-pointer rounded-full bg-black px-1.5 py-0.5 text-[10px] leading-none text-white"
					onclick={(e) => {
						e.stopPropagation();
						openDayView();
					}}
				>
					+{extraEventCount} more
				</button>
			{/if}
		</div>
	</div>
</div>

<style>
	.event-title {
		overflow: hidden;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		-webkit-box-orient: vertical;
	}
</style>
