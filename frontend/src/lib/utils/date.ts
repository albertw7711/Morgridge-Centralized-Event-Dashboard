export const MILLISECONDS_IN_DAY = 24 * 60 * 60 * 1000;

export function startOfDay(date: Date): Date {
	return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

export function addDays(date: Date, days: number): Date {
	return new Date(startOfDay(date).getTime() + days * MILLISECONDS_IN_DAY);
}

export function getWeekStart(date: Date): Date {
	const normalizedDate = startOfDay(date);
	return addDays(normalizedDate, -normalizedDate.getDay());
}

export function getWeekEnd(date: Date): Date {
	return addDays(getWeekStart(date), 6);
}

export function toLocalIsoDate(value: Date): string {
	const year = value.getFullYear();
	const month = String(value.getMonth() + 1).padStart(2, '0');
	const day = String(value.getDate()).padStart(2, '0');
	return `${year}-${month}-${day}`;
}

export function parseIsoDate(value: string): Date {
	const [yearText, monthText, dayText] = value.split('-');
	const year = Number(yearText);
	const month = Number(monthText);
	const day = Number(dayText);
	return new Date(year, month - 1, day);
}

export function isValidIsoDate(value: string): boolean {
	if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
		return false;
	}

	const parsedDate = parseIsoDate(value);
	return toLocalIsoDate(parsedDate) === value;
}