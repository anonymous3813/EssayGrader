<script>
	import { onMount } from 'svelte';
	import TemplateDropdown from './TemplateDropdown.svelte';
	import { templatesOptions } from '$lib/types';

	let { criteriaList = $bindable([]) } = $props();

	function generateId() {
		return Math.random().toString(36).slice(2, 9);
	}

	let customTemplates = $state([]);
	let allTemplates = $derived([...templatesOptions, ...customTemplates]);

	onMount(() => {
		const stored = localStorage.getItem('saved_rubrics');
		if (stored) {
			try {
				customTemplates = JSON.parse(stored);
			} catch (e) {
                console.error(e);
            }
		}
	});

	let baseTemplate = $state(null);
	let selectedTemplate = $state('');

	function loadTemplate(id) {
		const t = allTemplates.find((t) => t.id === id);
		if (!t) return;

		baseTemplate = t;
		criteriaList = t.criteria.map((c) => ({
			...c,
			id: generateId()
		}));
	}
	let isModified = $derived(() => {
		if (!baseTemplate) return false;

		if (criteriaList.length !== baseTemplate.criteria.length) return true;

		return criteriaList.some((c, i) => {
			const b = baseTemplate.criteria[i];
			if (!b) return true;

			return (
				c.name !== b.name ||
				c.description !== b.description ||
				c.weight !== b.weight ||
				c.possible_points !== b.possible_points
			);
		});
	});

	let canSave = $derived(criteriaList.length > 0 && (!baseTemplate || isModified()));
	let isSaving = $state(false);
	let newTemplateName = $state('');

	function saveCustomTemplate() {
		if (!newTemplateName.trim()) return;

		const newTemplate = {
			id: 'custom-' + generateId(),
			label: newTemplateName.trim(),
			criteria: criteriaList.map(c => ({...c}))
		};

		customTemplates = [...customTemplates, newTemplate];
		localStorage.setItem('saved_rubrics', JSON.stringify(customTemplates));

		selectedTemplate = newTemplate.id;
		baseTemplate = newTemplate;
		isSaving = false;
		newTemplateName = '';
	}

	function addCriterion() {
		criteriaList = [
			...criteriaList,
			{
				id: generateId(),
				name: '',
				description: '',
				weight: 1,
				possible_points: 10
			}
		];
	}

	function removeCriterion(id) {
		criteriaList = criteriaList.filter((c) => c.id !== id);
	}

	let totalPoints = $derived(
		criteriaList.reduce((sum, c) => sum + (c.possible_points || 0) * (c.weight || 0), 0)
	);
</script>

<section class="rubric">
	<!-- Templates -->
	<div class="top-bar">
		<div class="template-selector-wrap">
			<TemplateDropdown
				options={allTemplates.map((t) => ({
					...t,
					label: t.id === selectedTemplate && isModified() ? `${t.label} (modified)` : t.label
				}))}
				bind:value={selectedTemplate}
				onSelect={loadTemplate}
			/>
		</div>
		
		{#if canSave}
			<button class="save-btn" onclick={() => isSaving = !isSaving}>
				Save As
			</button>
		{/if}
	</div>

	{#if isSaving}
		<div class="save-row">
			<input class="save-input" placeholder="Custom name..." bind:value={newTemplateName} />
			<button class="confirm-btn" onclick={saveCustomTemplate}>Save</button>
			<button class="cancel-btn" onclick={() => isSaving = false}>Cancel</button>
		</div>
	{/if}

	<!-- Blocks -->
	<div class="blocks">
		{#each criteriaList as c, i (c.id)}
			<div class="block">
				<div class="handle">⋮⋮</div>

				<div class="content">
					<div class="title-row">
						<input class="title" placeholder="Criterion name" bind:value={c.name} />

						<div class="meta">
							<input
								type="number"
								bind:value={c.possible_points}
								class="num-input"
								min="0"
								title="Possible Points"
							/>
							pts ×
							<input
								type="number"
								bind:value={c.weight}
								class="num-input"
								min="0"
								step="0.1"
								title="Weight"
							/> wt
						</div>
					</div>

					<textarea class="desc" rows="1" placeholder="Description..." bind:value={c.description}></textarea>

					<div class="actions">
						<button onclick={() => removeCriterion(c.id)}>Remove</button>
					</div>
				</div>
			</div>
		{/each}
	</div>

	<button class="add" onclick={addCriterion}> + Add criterion </button>

	<div class="total">
		Total: {totalPoints}
	</div>
</section>

<style>
	.rubric {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.top-bar {
		display: flex;
		gap: 0.75rem;
		align-items: center;
		z-index: 10;
	}

	/* Template Selector */
	.template-selector-wrap {
		position: relative;
		flex: 1;
	}

	.save-btn {
		white-space: nowrap;
		padding: 0.6rem 1rem;
		background: rgba(200, 245, 90, 0.1);
		color: var(--accent);
		border: 1px solid rgba(200, 245, 90, 0.3);
		border-radius: 8px;
		font-family: var(--font-sans);
		font-size: 0.85rem;
		cursor: pointer;
		transition: all 0.2s;
	}
	.save-btn:hover {
		background: rgba(200, 245, 90, 0.2);
	}

	.save-row {
		display: flex;
		gap: 0.5rem;
		align-items: center;
		background: var(--surface-2);
		padding: 0.5rem;
		border-radius: 8px;
		border: 1px solid var(--border);
	}

	.save-input {
		flex: 1;
		background: transparent;
		border: none;
		outline: none;
		color: var(--ink);
		font-size: 0.85rem;
		font-family: var(--font-sans);
		padding: 0.25rem 0.5rem;
	}

	.confirm-btn {
		background: var(--accent);
		color: #000;
		border: none;
		border-radius: 4px;
		padding: 0.3rem 0.7rem;
		font-size: 0.75rem;
		font-weight: 600;
		cursor: pointer;
	}
	
	.cancel-btn {
		background: transparent;
		color: var(--ink-muted);
		border: none;
		border-radius: 4px;
		padding: 0.3rem 0.5rem;
		font-size: 0.75rem;
		cursor: pointer;
	}
	.cancel-btn:hover {
		color: var(--ink);
	}

	/* blocks */
	.blocks {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.block {
		display: flex;
		gap: 0.5rem;
		padding: 0.6rem;
		border-radius: 8px;
		transition: background 0.15s ease;
	}

	.block:hover {
		background: rgba(255, 255, 255, 0.03);
	}

	.handle {
		width: 18px;
		color: var(--ink-muted);
		opacity: 0.5;
	}

	.content {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.title-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.title {
		background: transparent;
		border: none;
		outline: none;
		font-weight: 600;
		color: var(--ink);
		width: 100%;
	}

	.desc {
		background: transparent;
		border: none;
		outline: none;
		color: var(--ink-muted);
		resize: none;
	}

	.meta {
		font-size: 0.75rem;
		color: var(--ink-muted);
		display: flex;
		align-items: center;
		gap: 0.25rem;
		white-space: nowrap;
	}

	.num-input {
		background: rgba(0, 0, 0, 0.2);
		border: 1px solid var(--border);
		border-radius: 4px;
		color: var(--ink);
		width: 45px;
		padding: 0.2rem 0.3rem;
		text-align: center;
		font-size: 0.75rem;
		outline: none;
		transition: border-color 0.2s;
	}

	.num-input:focus {
		border-color: rgba(200, 245, 90, 0.4);
	}

	.num-input::-webkit-outer-spin-button,
	.num-input::-webkit-inner-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
	.num-input[type='number'] {
		appearance: textfield;
		-moz-appearance: textfield;
	}

	.actions button {
		background: transparent;
		border: none;
		color: #ff6b6b;
		cursor: pointer;
	}

	.add {
		border: 1px dashed var(--border);
		background: transparent;
		padding: 0.6rem;
		border-radius: 8px;
		cursor: pointer;
	}

	.total {
		text-align: right;
		font-size: 0.85rem;
		color: var(--accent);
	}
</style>
