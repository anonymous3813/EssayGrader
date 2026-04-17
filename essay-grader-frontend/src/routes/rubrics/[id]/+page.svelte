<script>
	import { page } from '$app/stores';
	import { templatesOptions } from '$lib/types';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	let rubric = $state(null);
	let mounted = $state(false);

	onMount(() => {
		mounted = true;
		const id = $page.params.id;

		// check standard templates
		let found = templatesOptions.find((t) => t.id === id);

		if (!found) {
			// check custom templates
			const stored = localStorage.getItem('saved_rubrics');
			if (stored) {
				try {
					const custom = JSON.parse(stored);
					found = custom.find((r) => r.id === id);
				} catch (e) {
					console.error(e);
				}
			}
		}

		if (found) {
			rubric = found;
		} else {
			// Not found
			goto('/rubrics');
		}
	});

	let totalPoints = $derived(
		rubric
			? rubric.criteria.reduce((sum, c) => sum + (c.possible_points || 0) * (c.weight || 1), 0)
			: 0
	);
</script>

<div class="root" class:mounted>
	<div class="bg-grid" aria-hidden="true"></div>
	<div class="bg-glow" aria-hidden="true"></div>

	<main class="page" class:mounted>
		{#if rubric}
			<div class="page-header">
				<a href="/rubrics" class="back-link">← Back to library</a>
				<div class="hero-label">Preview Rubric</div>

				<div class="title-row">
					<h1>{rubric.label || rubric.name}</h1>
					<a href="/grade?rubric={rubric.id}" class="use-btn">Use this rubric →</a>
				</div>
				<div class="tags">
					{#if rubric.tags && rubric.tags.length > 0}
						{#each rubric.tags as tag}
							<span class="tag">{tag}</span>
						{/each}
					{:else}
						<span class="tag custom-tag">Custom</span>
					{/if}
				</div>

				<p class="desc">
					{rubric.desc || 'A collection of criteria used for assessing essay quality.'}
				</p>
				<div class="total-score">
					Total Possible Score: <span class="score-num">{totalPoints}</span>
				</div>
			</div>

			<section class="criteria-list">
				{#each rubric.criteria as crit, i}
					<div class="crit-card" style="--i:{i}">
						<div class="crit-header">
							<div class="crit-number">{(i + 1).toString().padStart(2, '0')}</div>
							<h2>{crit.name}</h2>
						</div>
						<p class="crit-desc">{crit.description}</p>
						<div class="crit-meta">
							<div class="meta-item">
								<span class="meta-label">Possible Points:</span>
								<span class="meta-val">{crit.possible_points || 0}</span>
							</div>
							<div class="meta-item">
								<span class="meta-label">Weight:</span>
								<span class="meta-val">{crit.weight || 1}x</span>
							</div>
						</div>
					</div>
				{/each}
			</section>
		{/if}
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
		padding-bottom: 5rem;
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

	.title-row {
		display: flex;
		gap: 1rem;
		align-items: center;
		justify-content: space-between;
		width: 100%;
		flex-wrap: wrap;
	}

	h1 {
		font-family: var(--font-display);
		font-size: clamp(2rem, 4vw, 2.5rem);
		line-height: 1.1;
		margin: 0;
	}

	.use-btn {
		background: var(--accent);
		color: #0d0f0e;
		border: none;
		padding: 0.75rem 1.25rem;
		font-family: var(--font-sans);
		font-weight: 600;
		font-size: 0.95rem;
		border-radius: 8px;
		cursor: pointer;
		text-decoration: none;
		transition: background 0.2s;
		white-space: nowrap;
	}
	.use-btn:hover {
		background: var(--accent-dim);
	}

	.tags {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		margin-top: 0.5rem;
	}

	.tag {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		letter-spacing: 0.05em;
		padding: 0.2rem 0.6rem;
		border-radius: 4px;
		background: rgba(255, 255, 255, 0.05);
		color: var(--ink-muted);
		text-transform: uppercase;
	}
	.custom-tag {
		background: rgba(200, 245, 90, 0.08);
		color: var(--accent);
	}

	.desc {
		color: var(--ink-muted);
		font-size: 1rem;
		line-height: 1.6;
		margin-top: 0.5rem;
	}

	.total-score {
		margin-top: 1rem;
		font-size: 1.1rem;
		font-family: var(--font-sans);
		color: var(--ink);
		padding: 0.75rem 1.25rem;
		background: var(--surface);
		border-radius: 8px;
		border: 1px solid var(--border);
		display: inline-block;
		width: fit-content;
	}

	.score-num {
		font-family: var(--font-mono);
		color: var(--accent);
		font-size: 1.25rem;
		margin-left: 0.5rem;
		font-weight: bold;
	}

	.criteria-list {
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
		margin-top: 1.5rem;
	}

	.crit-card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 12px;
		padding: 1.75rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
		opacity: 0;
		transform: translateY(12px);
		transition:
			opacity 0.4s ease calc(var(--i) * 0.07s),
			transform 0.4s ease calc(var(--i) * 0.07s),
			border-color 0.2s;
	}

	.mounted .crit-card {
		opacity: 1;
		transform: translateY(0);
	}

	.crit-card:hover {
		border-color: rgba(200, 245, 90, 0.15);
	}

	.crit-header {
		display: flex;
		align-items: center;
		gap: 1rem;
	}

	.crit-number {
		font-family: var(--font-mono);
		font-size: 1.2rem;
		color: var(--accent);
		opacity: 0.8;
	}

	.crit-header h2 {
		font-family: var(--font-display);
		font-size: 1.4rem;
		color: var(--ink);
		margin: 0;
	}

	.crit-desc {
		color: var(--ink-muted);
		font-size: 0.95rem;
		line-height: 1.6;
		margin: 0;
	}

	.crit-meta {
		display: flex;
		gap: 2rem;
		margin-top: 0.5rem;
		padding-top: 1rem;
		border-top: 1px dashed rgba(255, 255, 255, 0.08);
	}

	.meta-item {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.meta-label {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--ink-muted);
	}

	.meta-val {
		font-size: 1.1rem;
		font-weight: 500;
		color: var(--ink);
	}
</style>
