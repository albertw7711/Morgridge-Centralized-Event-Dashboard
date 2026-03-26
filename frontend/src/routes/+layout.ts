import type { LayoutLoad } from './$types';
import { mockEvents } from '$lib/mockEvents';

export const load: LayoutLoad = () => {
	return {
		events: mockEvents
	};
};
