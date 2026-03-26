import type { CalendarStepMode } from '$lib/stores/calendar-ui';
import { addDays, getWeekEnd, getWeekStart } from '$lib/utils/date';

export type CalendarDisplayDay = {
	date: Date;
	dayNumber: number;
	isCurrentMonth: boolean;
};

export const CALENDAR_WEEKDAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

export function buildMonthCalendarDays(referenceDate: Date): CalendarDisplayDay[] {
	const displayedYear = referenceDate.getFullYear();
	const displayedMonth = referenceDate.getMonth();
	const firstDayOfMonth = new Date(displayedYear, displayedMonth, 1);
	const firstVisibleDate = addDays(firstDayOfMonth, -firstDayOfMonth.getDay());

	return Array.from({ length: 42 }, (_, index) => {
		const date = addDays(firstVisibleDate, index);
		return {
			date,
			dayNumber: date.getDate(),
			isCurrentMonth: date.getMonth() === displayedMonth
		};
	});
}

export function chunkCalendarWeeks(days: CalendarDisplayDay[]): CalendarDisplayDay[][] {
	return Array.from({ length: 6 }, (_, weekIndex) =>
		days.slice(weekIndex * 7, (weekIndex + 1) * 7)
	);
}

export function buildCurrentWeekDays(referenceDate: Date): CalendarDisplayDay[] {
	const displayedMonth = referenceDate.getMonth();
	const weekStart = getWeekStart(referenceDate);

	return Array.from({ length: 7 }, (_, index) => {
		const date = addDays(weekStart, index);
		return {
			date,
			dayNumber: date.getDate(),
			isCurrentMonth: date.getMonth() === displayedMonth
		};
	});
}

export function formatPeriodLabel(date: Date, mode: CalendarStepMode): string {
	if (mode === 'month') {
		return new Intl.DateTimeFormat('en-US', { month: 'long', year: 'numeric' }).format(date);
	}

	if (mode === 'day') {
		return new Intl.DateTimeFormat('en-US', {
			weekday: 'short',
			month: 'short',
			day: 'numeric',
			year: 'numeric'
		}).format(date);
	}

	const weekStart = getWeekStart(date);
	const weekEnd = getWeekEnd(date);
	const shortFormatter = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric' });
	return `${shortFormatter.format(weekStart)} - ${shortFormatter.format(weekEnd)}`;
}
