<script>
    
	let { options = [], value = $bindable(''), onSelect = () => {} } = $props();

	let open = $state(false);

	function selectOption(opt) {
		value = opt.id;
		onSelect(opt.id);
		open = false;
	}

	function toggle() {
		open = !open;
	}

	function close() {
		open = false;
	}
</script>

<div class="dropdown">
	<!-- trigger -->
	<button class="trigger" type="button" onclick={toggle}>
		{#if value}
			{options.find((o) => o.id === value)?.label ?? 'Select template'}
		{:else}
			Select template
		{/if}

		<span class="chev">▾</span>
	</button>

	<!-- menu -->
	{#if open}
		<div class="menu">
			{#each options as opt (opt.id)}
				<button
					class="item"
					type="button"
					onclick={() => {
						toggle();
						selectOption(opt);
					}}
				>
					<div class="label">{opt.label}</div>
					<div class="sub">{opt.criteria.length} criteria</div>
				</button>
			{/each}
		</div>
	{/if}
</div>

<style>
	.dropdown {
		position: relative;
		width: 100%;
	}

	.trigger {
		width: 100%;
		padding: 0.75rem 1rem;
		background: var(--surface-2);
		border: 1px solid var(--border);
		border-radius: 10px;
		color: var(--ink);
		display: flex;
		justify-content: space-between;
		align-items: center;
		cursor: pointer;
		font-size: 0.9rem;
	}

	.trigger:hover {
		border-color: rgba(200, 245, 90, 0.35);
	}

	.chev {
		color: var(--ink-muted);
	}

	.menu {
		position: absolute;
		top: calc(100% + 6px);
		left: 0;
		right: 0;
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 12px;
		z-index: 50;
		overflow: hidden;
		box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
	}

	.item {
		width: 100%;
		text-align: left;
		padding: 0.75rem 1rem;
		background: transparent;
		border: none;
		color: var(--ink);
		cursor: pointer;
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.item:hover {
		background: rgba(255, 255, 255, 0.05);
	}

	.label {
		font-size: 0.9rem;
	}

	.sub {
		font-size: 0.75rem;
		color: var(--ink-muted);
	}
</style>
