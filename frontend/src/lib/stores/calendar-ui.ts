import { writable } from 'svelte/store';

export type CalendarStepMode = 'month' | 'week' | 'day';

export const calendarReferenceDate = writable(new Date());
export const calendarStepMode = writable<CalendarStepMode>('month');
export const calendarSearchQuery = writable('');
export const pizzaOnlyFilter = writable(false);
export const expandedDayEventId = writable<number | null>(null);

export function shiftCalendarReferenceDate(
	current: Date,
	mode: CalendarStepMode,
	delta: number
): Date {
	const nextDate = new Date(current);

	if (mode === 'month') {
		nextDate.setMonth(nextDate.getMonth() + delta);
		return nextDate;
	}

	if (mode === 'day') {
		nextDate.setDate(nextDate.getDate() + delta);
		return nextDate;
	}

	nextDate.setDate(nextDate.getDate() + 7 * delta);
	return nextDate;
}
