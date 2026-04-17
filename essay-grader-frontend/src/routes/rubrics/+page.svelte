<script>
	import { onMount } from 'svelte';
	import { templatesOptions as templates } from '$lib/types';

	let mounted = $state(false);

	onMount(() => {
		mounted = true;
	});

	let customRubrics = $state([]);

	onMount(() => {
		mounted = true;
		const stored = localStorage.getItem('saved_rubrics');
		if (stored) {
			try {
				customRubrics = JSON.parse(stored);
			} catch (e) {
				console.error(e);
			}
		}
	});

	function deleteRubric(id) {
		customRubrics = customRubrics.filter((r) => r.id !== id);
		localStorage.setItem('saved_rubrics', JSON.stringify(customRubrics));
	}
</script>

<div class="root" class:mounted>
	<div class="bg-grid" aria-hidden="true"></div>
	<div class="bg-glow" aria-hidden="true"></div>

	<main class="page" class:mounted>
		<div class="page-header">
			<div class="hero-label">Rubric Library</div>
			<div class="header-row">
				<h1>Your rubrics</h1>
				<a href="/rubrics/new" class="new-btn"> ＋ New rubric </a>
			</div>
			<p class="page-sub">
				Choose a template or manage your custom rubrics. Rubrics are used when grading essays.
			</p>
		</div>

		<!-- Templates -->
		<section class="rubric-section">
			<h2 class="section-title">
				<span class="section-num">Templates</span>
			</h2>
			<div class="rubric-grid">
				{#each templates as t, i (t.id)}
					<div class="rubric-card" style="--i:{i}">
						<div class="rubric-card-top">
							<h3>{t.label}</h3>
							<div class="tag-row">
								{#each t.tags as tag}
									<span class="tag">{tag}</span>
								{/each}
							</div>
						</div>
						<p class="rubric-desc">{t.desc}</p>
						<div class="rubric-card-footer">
							<a href="/grade?rubric={t.id}" class="use-btn">Use this →</a>
							<a href="/rubrics/{t.id}" class="preview-link">Preview</a>
						</div>
					</div>
				{/each}
			</div>
		</section>

		<!-- Custom -->
		<section class="rubric-section">
			<h2 class="section-title">
				<span class="section-num">Your custom rubrics</span>
			</h2>
			{#if customRubrics.length === 0}
				<div class="empty-state">
					<p>No custom rubrics yet.</p>
					<a href="/rubrics/new" class="new-btn-sm">Create one →</a>
				</div>
			{:else}
				<div class="rubric-grid">
					{#each customRubrics as r, i (r.id)}
						<div class="rubric-card custom" style="--i:{i}">
							<div class="rubric-card-top">
								<h3>{r.label}</h3>
								<div class="tag-row">
									<span class="tag custom-tag">Custom</span>
									{#if r.tags}
										{#each r.tags as tag}
											<span class="tag custom-tag">{tag}</span>
										{/each}
									{/if}
								</div>
							</div>
							<p class="rubric-desc">
								{r.desc || (r.criteria ? r.criteria.length + ' criteria defined.' : '')}
							</p>
							<div class="rubric-card-footer">
								<a href="/grade?rubric={r.id}" class="use-btn">Use this →</a>
								<div class="footer-actions">
									<a href="/rubrics/edit/{r.id}" class="preview-link">Edit</a>
									<button class="delete-btn" onclick={() => deleteRubric(r.id)}>Delete</button>
								</div>
							</div>
						</div>
					{/each}
				</div>
			{/if}
		</section>
	</main>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

	:global(*, *::before, *::after) {
		box-sizing: border-box;
		margin: 0;
		padding: 0;
	}
	:global(body) {
		background: #0d0f0e;
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
		max-width: 1100px;
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
	}
	.hero-label {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		color: var(--accent);
		letter-spacing: 0.12em;
		text-transform: uppercase;
		margin-bottom: 0.75rem;
	}
	.header-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-bottom: 0.5rem;
	}
	h1 {
		font-family: var(--font-display);
		font-size: clamp(2rem, 4vw, 3rem);
		line-height: 1.1;
	}
	.page-sub {
		color: var(--ink-muted);
		font-size: 0.95rem;
	}

	.new-btn {
		background: var(--accent);
		color: #0d0f0e;
		text-decoration: none;
		padding: 0.45rem 1.1rem;
		border-radius: 6px;
		font-weight: 500;
		font-size: 0.875rem;
		transition: background 0.2s;
		white-space: nowrap;
	}
	.new-btn:hover {
		background: var(--accent-dim);
	}

	.rubric-section {
		margin-bottom: 3rem;
	}
	.section-title {
		margin-bottom: 1rem;
	}
	.section-num {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		color: var(--ink-muted);
		letter-spacing: 0.1em;
		text-transform: uppercase;
	}

	.rubric-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
		gap: 1rem;
	}

	.rubric-card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 10px;
		padding: 1.25rem;
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		opacity: 0;
		transform: translateY(12px);
		transition:
			opacity 0.4s ease calc(var(--i) * 0.07s),
			transform 0.4s ease calc(var(--i) * 0.07s),
			border-color 0.2s;
	}
	.mounted .rubric-card {
		opacity: 1;
		transform: translateY(0);
	}
	.rubric-card:hover {
		border-color: rgba(200, 245, 90, 0.2);
	}
	.rubric-card.custom {
		border-color: rgba(200, 245, 90, 0.12);
	}

	.rubric-card-top {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}
	.rubric-card h3 {
		font-family: var(--font-display);
		font-size: 1rem;
		color: var(--ink);
	}
	.tag-row {
		display: flex;
		gap: 0.35rem;
		flex-wrap: wrap;
	}
	.tag {
		font-family: var(--font-mono);
		font-size: 0.65rem;
		letter-spacing: 0.06em;
		padding: 0.15rem 0.5rem;
		border-radius: 4px;
		background: rgba(255, 255, 255, 0.05);
		color: var(--ink-muted);
		text-transform: uppercase;
	}
	.custom-tag {
		background: rgba(200, 245, 90, 0.08);
		color: var(--accent);
	}

	.rubric-desc {
		font-size: 0.85rem;
		color: var(--ink-muted);
		line-height: 1.5;
		flex: 1;
	}

	.rubric-card-footer {
		display: flex;
		align-items: center;
		justify-content: space-between;
		margin-top: auto;
	}
	.use-btn {
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--accent);
		text-decoration: none;
		transition: color 0.2s;
	}
	.use-btn:hover {
		color: var(--accent-dim);
	}
	.preview-link {
		font-size: 0.8rem;
		color: var(--ink-muted);
		text-decoration: none;
		transition: color 0.2s;
	}
	.preview-link:hover {
		color: var(--ink);
	}

	.empty-state {
		padding: 2rem;
		border: 1px dashed var(--border);
		border-radius: 10px;
		text-align: center;
		color: var(--ink-muted);
		font-size: 0.9rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
	}
	.new-btn-sm {
		font-family: var(--font-mono);
		font-size: 0.8rem;
		color: var(--accent);
		text-decoration: none;
	}

	.footer-actions {
		display: flex;
		gap: 0.75rem;
		align-items: center;
	}

	.delete-btn {
		background: transparent;
		color: rgba(255, 107, 107, 0.7);
		border: 1px solid rgba(255, 107, 107, 0.3);
		border-radius: 4px;
		padding: 0.15rem 0.4rem;
		font-size: 0.75rem;
		cursor: pointer;
		transition: all 0.2s;
	}
	.delete-btn:hover {
		color: #ff6b6b;
		border-color: rgba(255, 107, 107, 0.6);
		background: rgba(255, 107, 107, 0.05);
	}
</style>
