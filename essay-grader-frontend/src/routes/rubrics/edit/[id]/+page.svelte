<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import RubricBuilder from '$lib/components/RubricBuilder.svelte';
	import { goto } from '$app/navigation';

	let rubricId = $derived($page.params.id);
	let rubricName = $state('');
	let criteriaList = $state([]);
	let mounted = $state(false);

	onMount(() => {
		mounted = true;
		const stored = localStorage.getItem('saved_rubrics');
		if (stored) {
			const rubrics = JSON.parse(stored);
			const target = rubrics.find(r => r.id === rubricId);
			if (target) {
				rubricName = target.label;
				// deep copy criteria so Svelte keys won't conflict
				criteriaList = target.criteria.map(c => ({...c}));
			} else {
				// Not found
				goto('/rubrics');
			}
		}
	});

	function saveEdits() {
		if (!rubricName.trim()) {
			alert('Please provide a name for this rubric.');
			return;
		}
		const stored = localStorage.getItem('saved_rubrics');
		if (stored) {
			let rubrics = JSON.parse(stored);
			const idx = rubrics.findIndex(r => r.id === rubricId);
			if (idx !== -1) {
				rubrics[idx].label = rubricName.trim();
				rubrics[idx].criteria = criteriaList.map(c => ({...c}));
				rubrics[idx].desc = criteriaList.length + ' criteria defined.';
				
				localStorage.setItem('saved_rubrics', JSON.stringify(rubrics));
				goto('/rubrics');
			}
		}
	}
</script>

<div class="root" class:mounted>
	<div class="bg-grid" aria-hidden="true"></div>
	<div class="bg-glow" aria-hidden="true"></div>

	<main class="page" class:mounted>
		<div class="page-header">
			<a href="/rubrics" class="back-link">← Back to library</a>
			<div class="hero-label">Editing</div>
			
			<div class="name-editor">
				<input class="name-input" bind:value={rubricName} placeholder="Custom Rubric Name..." />
				<button class="save-master-btn" onclick={saveEdits}>Save Changes</button>
			</div>
		</div>

		<section class="section-card">
			<RubricBuilder bind:criteriaList />
		</section>
	</main>
</div>

<style>
	:global(body) {
		background: #0d0f0e;
		color: #f0ede6;
		margin: 0;
	}

	.root {
		--ink: #f0ede6;
		--ink-muted: #8a897f;
		--accent: #c8f55a;
		--accent-dim: #9cbf3a;
		--surface: #161a17;
		--surface-2: #1c211e;
		--border: rgba(255, 255, 255, 0.07);
		--font-display: 'DM Serif Display', Georgia, serif;
		--font-sans: 'DM Sans', sans-serif;
		--font-mono: 'DM Mono', monospace;

		min-height: 100vh;
		background: #0d0f0e;
		color: var(--ink);
		font-family: var(--font-sans);
		position: relative;
		overflow-x: hidden;
	}

	.bg-grid {
		position: fixed;
		inset: 0;
		pointer-events: none;
		z-index: 0;
		background-image:
			linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
			linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
		background-size: 48px 48px;
	}
	.bg-glow {
		position: fixed;
		top: -20%;
		left: 50%;
		transform: translateX(-50%);
		width: 700px;
		height: 500px;
		pointer-events: none;
		z-index: 0;
		background: radial-gradient(ellipse at center, rgba(200, 245, 90, 0.07) 0%, transparent 70%);
	}

	.page {
		position: relative;
		z-index: 5;
		max-width: 900px;
		margin: 0 auto;
		padding: 3rem 2rem 5rem;
		opacity: 0;
		transform: translateY(16px);
		transition:
			opacity 0.6s ease,
			transform 0.6s ease;
	}
	.mounted .page,
	.page.mounted {
		opacity: 1;
		transform: translateY(0);
	}

	.page-header {
		margin-bottom: 2.5rem;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
	}
	
	.back-link {
		color: var(--ink-muted);
		text-decoration: none;
		font-size: 0.85rem;
		margin-bottom: 0.5rem;
		align-self: flex-start;
		transition: color 0.2s;
	}
	.back-link:hover {
		color: var(--ink);
	}

	.hero-label {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		color: var(--accent);
		letter-spacing: 0.12em;
		text-transform: uppercase;
	}

	.name-editor {
		display: flex;
		gap: 1rem;
		align-items: center;
		width: 100%;
	}

	.name-input {
		flex: 1;
		background: transparent;
		border: 1px dashed var(--border);
		border-radius: 8px;
		color: var(--ink);
		font-family: var(--font-display);
		font-size: clamp(2rem, 4vw, 2.5rem);
		padding: 0.75rem 1rem;
		outline: none;
		transition: border-color 0.2s, background 0.2s;
	}
	.name-input:focus {
		border-color: rgba(200, 245, 90, 0.5);
		background: rgba(255, 255, 255, 0.02);
	}

	.save-master-btn {
		background: var(--accent);
		color: #000;
		border: none;
		padding: 0.8rem 1.5rem;
		font-family: var(--font-sans);
		font-weight: 600;
		font-size: 0.95rem;
		border-radius: 8px;
		cursor: pointer;
		transition: background 0.2s;
		white-space: nowrap;
	}
	.save-master-btn:hover {
		background: var(--accent-dim);
	}

	.section-card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 12px;
		padding: 1.5rem;
	}
</style>
