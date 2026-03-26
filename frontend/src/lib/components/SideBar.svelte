<script lang="ts">
	import { buildSidebarGroups } from '$lib/features/events/sidebar';
	import { parseEventDate } from '$lib/features/events/utils';
	import {
		calendarReferenceDate,
		calendarStepMode,
		expandedDayEventId
	} from '$lib/stores/calendar-ui';
	import { allEvents } from '$lib/stores/events';

	const sidebarGroups = $derived(buildSidebarGroups(new Date(), $allEvents));

	function openSidebarEvent(eventDay: string, eventId: number): void {
		calendarReferenceDate.set(parseEventDate(eventDay));
		expandedDayEventId.set(eventId);
		calendarStepMode.set('day');
	}
</script>

<aside
	class="flex h-full w-full flex-col rounded-lg border border-(--uwGrayLight) bg-(--uwWhite) p-3 shadow-sm"
>
	<h2 class="px-1 text-sm font-semibold text-(--uwGrayDark)">Upcoming Events</h2>
	<div class="scrollbar-hidden mt-1 min-h-32 flex-1 overflow-y-scroll">
		{#each sidebarGroups as group (group.title)}
			<p
				class="mt-4 mb-1 px-1 text-[10px] font-semibold tracking-wider text-(--uwRedDark) uppercase first:mt-1"
			>
				{group.title}
			</p>
			{#if group.events.length > 0}
				{#each group.events as event (event.id)}
					<button
						type="button"
						onclick={() => openSidebarEvent(event.eventDay, event.id)}
						class="block w-full cursor-pointer rounded-lg border border-transparent px-2 py-2 text-left transition-colors hover:border-(--uwGrayLight) hover:bg-(--uwGrayLightest)"
					>
						<div class="flex items-start justify-between gap-2">
							<span class="text-sm leading-tight font-semibold text-(--uwGrayDark)">
								{event.eventTitle}{#if event.food}&nbsp;🍕{/if}
							</span>
							<span class="shrink-0 text-xs font-medium text-(--uwRedDark)"
								>{event.eventStartTime}</span
							>
						</div>
						<p class="mt-0.5 truncate text-xs text-(--uwGrayDark)/70">{event.eventLocation}</p>
					</button>
				{/each}
			{:else}
				<p class="px-1 text-xs text-(--uwGrayDark)/70">No matching events.</p>
			{/if}
		{/each}
	</div>
</aside>

<style>
	.scrollbar-hidden::-webkit-scrollbar {
		display: none;
	}
	.scrollbar-hidden {
		-ms-overflow-style: none;
		scrollbar-width: none;
	}
</style>
