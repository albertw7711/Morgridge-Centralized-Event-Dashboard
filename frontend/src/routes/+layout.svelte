<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import TopBar from '$lib/components/TopBar.svelte';
	import { setAllEvents } from '$lib/stores/events';

	let { children, data } = $props();

	$effect(() => {
		setAllEvents(data.events);
	});
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>

<div class="flex w-full flex-col gap-8 pb-8 lg:h-screen">
	<div class="flex-none">
		<TopBar events={data.events} />
	</div>
	<div class="min-h-0 flex-1">
		{@render children()}
	</div>
</div>
