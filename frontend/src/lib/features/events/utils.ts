import type { EventInfo } from '$lib/mockEvents';
import { parseIsoDate } from '$lib/utils/date';

export type EventSearchMatch = {
	key: 'title' | 'host' | 'room' | 'description' | 'date';
	label: 'Title' | 'Host' | 'Room' | 'Description' | 'Date';
	value: string;
};

export type EventSearchScope = 'preview' | 'full';

export type HighlightSegment = {
	text: string;
	matched: boolean;
};

export function parseEventDate(eventDay: string): Date {
	const [month, day, year] = eventDay.split('/').map(Number);
	return new Date(year, month - 1, day);
}

export function parseEventDateTime(event: Pick<EventInfo, 'eventDay' | 'eventStartTime'>): Date {
	const eventDate = parseEventDate(event.eventDay);
	const [timeValue, meridiem] = event.eventStartTime.split(' ');
	const [hourValue, minuteValue] = timeValue.split(':').map(Number);
	const hours = (hourValue % 12) + (meridiem === 'PM' ? 12 : 0);

	return new Date(
		eventDate.getFullYear(),
		eventDate.getMonth(),
		eventDate.getDate(),
		hours,
		minuteValue,
		0,
		0
	);
}

export function getEventRecencyScore(
	event: Pick<EventInfo, 'eventDay' | 'eventStartTime'>,
	referenceDate: Date = new Date()
): number {
	const eventTimestamp = parseEventDateTime(event).getTime();
	const referenceTimestamp = referenceDate.getTime();

	if (eventTimestamp < referenceTimestamp) {
		return Number.NEGATIVE_INFINITY;
	}

	return -(eventTimestamp - referenceTimestamp);
}

export function sortEventsChronologically<T extends Pick<EventInfo, 'eventDay' | 'eventStartTime'>>(
	events: T[]
): T[] {
	return [...events].sort(
		(firstEvent, secondEvent) =>
			parseEventDateTime(firstEvent).getTime() - parseEventDateTime(secondEvent).getTime()
	);
}

export function filterEventsByIsoDate<T extends Pick<EventInfo, 'eventDay'>>(
	events: T[],
	selectedDate: string | null
): T[] {
	if (!selectedDate) {
		return [];
	}

	const selectedTime = parseIsoDate(selectedDate).getTime();
	return events.filter((event) => parseEventDate(event.eventDay).getTime() === selectedTime);
}

export function filterEventsBySearchQuery<T extends EventInfo>(
	events: T[],
	query: string,
	scope: EventSearchScope = 'full'
): T[] {
	const normalizedQuery = query.trim().toLowerCase();

	if (!normalizedQuery) {
		return events;
	}

	return events.filter((event) => getEventSearchMatches(event, normalizedQuery, scope).length > 0);
}

export function getEventSearchMatches<T extends EventInfo>(
	event: T,
	query: string,
	scope: EventSearchScope = 'full'
): EventSearchMatch[] {
	const normalizedQuery = query.trim().toLowerCase();

	if (!normalizedQuery) {
		return [];
	}

	const fieldMatches: EventSearchMatch[] = [
		{ key: 'title', label: 'Title', value: event.eventTitle },
		{ key: 'host', label: 'Host', value: event.eventHost },
		{ key: 'room', label: 'Room', value: event.eventLocation },
		{ key: 'description', label: 'Description', value: event.eventDescription },
		{ key: 'date', label: 'Date', value: event.eventDay }
	];

	const allowedKeys =
		scope === 'preview'
			? new Set<EventSearchMatch['key']>(['title', 'host', 'room'])
			: new Set<EventSearchMatch['key']>(['title', 'host', 'room', 'description', 'date']);

	return fieldMatches.filter(
		(match) => allowedKeys.has(match.key) && match.value.toLowerCase().includes(normalizedQuery)
	);
}

export function buildHighlightSegments(text: string, query: string): HighlightSegment[] {
	const normalizedQuery = query.trim().toLowerCase();

	if (!normalizedQuery) {
		return [{ text, matched: false }];
	}

	const segments: HighlightSegment[] = [];
	const source = text;
	const loweredSource = source.toLowerCase();
	const needleLength = normalizedQuery.length;

	let cursor = 0;
	while (cursor < source.length) {
		const matchIndex = loweredSource.indexOf(normalizedQuery, cursor);

		if (matchIndex === -1) {
			segments.push({ text: source.slice(cursor), matched: false });
			break;
		}

		if (matchIndex > cursor) {
			segments.push({ text: source.slice(cursor, matchIndex), matched: false });
		}

		segments.push({ text: source.slice(matchIndex, matchIndex + needleLength), matched: true });
		cursor = matchIndex + needleLength;
	}

	return segments.filter((segment) => segment.text.length > 0);
}

export function countEventsOnIsoDate<T extends Pick<EventInfo, 'eventDay'>>(
	events: T[],
	selectedDate: string
): number {
	return filterEventsByIsoDate(events, selectedDate).length;
}
