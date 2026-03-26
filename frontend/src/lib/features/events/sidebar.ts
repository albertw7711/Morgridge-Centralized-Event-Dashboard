import type { EventInfo } from '$lib/mockEvents';
import { addDays, getWeekEnd, startOfDay } from '$lib/utils/date';
import { parseEventDate } from '$lib/features/events/utils';

export type SidebarGroup = {
	title: 'Today' | 'Tomorrow' | 'This Week';
	events: EventInfo[];
};

export function buildSidebarGroups(referenceDate: Date, events: EventInfo[]): SidebarGroup[] {
	const today = startOfDay(referenceDate);
	const tomorrow = addDays(today, 1);
	const weekEnd = getWeekEnd(today);

	return [
		{
			title: 'Today',
			events: events.filter((event) => parseEventDate(event.eventDay).getTime() === today.getTime())
		},
		{
			title: 'Tomorrow',
			events: events.filter(
				(event) => parseEventDate(event.eventDay).getTime() === tomorrow.getTime()
			)
		},
		{
			title: 'This Week',
			events: events.filter((event) => {
				const eventDate = parseEventDate(event.eventDay);
				return eventDate > tomorrow && eventDate <= weekEnd;
			})
		}
	];
}