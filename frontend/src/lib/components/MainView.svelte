<script lang="ts">
	import Calendar from '$lib/components/Calendar.svelte';
	import DayView from '$lib/components/DayView.svelte';
	import { toLocalIsoDate } from '$lib/utils/date';
	import {
		calendarReferenceDate,
		calendarStepMode,
		expandedDayEventId
	} from '$lib/stores/calendar-ui';

	const selectedDate = $derived(toLocalIsoDate($calendarReferenceDate));
</script>

{#if $calendarStepMode === 'day'}
	<DayView {selectedDate} expandedEventId={$expandedDayEventId} />
{:else}
	<Calendar />
{/if}
