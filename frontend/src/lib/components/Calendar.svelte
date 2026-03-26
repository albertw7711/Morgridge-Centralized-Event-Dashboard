<script lang="ts">
	import {
		buildCurrentWeekDays,
		buildMonthCalendarDays,
		CALENDAR_WEEKDAY_LABELS,
		chunkCalendarWeeks
	} from '$lib/features/calendar/view';
	import CalendarDayBlock from '$lib/components/CalendarDayBlock.svelte';
	import { calendarReferenceDate, calendarStepMode } from '$lib/stores/calendar-ui';

	const calendarDays = $derived(buildMonthCalendarDays($calendarReferenceDate));
	const weeks = $derived(chunkCalendarWeeks(calendarDays));
	const currentWeekDays = $derived(buildCurrentWeekDays($calendarReferenceDate));
</script>

<div class="h-full w-full">
	<table class="calendar-table h-full w-full table-fixed border-collapse">
		<thead>
			<tr>
				{#each CALENDAR_WEEKDAY_LABELS as day (day)}
					<th class="pb-4 font-medium">{day}</th>
				{/each}
			</tr>
		</thead>
		{#if $calendarStepMode === 'week'}
			<tbody class="week-body">
				<tr>
					{#each currentWeekDays as day (day.date.getTime())}
						<td class="p-0 align-top">
							<div class={`h-full w-full ${day.isCurrentMonth ? '' : 'opacity-40'}`}>
								<CalendarDayBlock date={day.date} dayNumber={day.dayNumber} />
							</div>
						</td>
					{/each}
				</tr>
			</tbody>
		{:else}
			<tbody class="month-body">
				{#each weeks as week, weekIndex (weekIndex)}
					<tr>
						{#each week as day (day.date.getTime())}
							<td class="p-0 align-top">
								<div class={`h-full w-full ${day.isCurrentMonth ? '' : 'opacity-40'}`}>
									<CalendarDayBlock date={day.date} dayNumber={day.dayNumber} />
								</div>
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		{/if}
	</table>
</div>

<style>
	.calendar-table {
		height: 100%;
	}

	.calendar-table thead {
		height: 2.5rem;
	}

	.calendar-table tbody {
		height: calc(100% - 2.5rem);
	}

	.calendar-table tbody.week-body > tr {
		height: 100%;
	}

	.calendar-table tbody.month-body > tr {
		height: 16.6667%;
	}
</style>
