<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import RubricBuilder from '$lib/components/RubricBuilder.svelte';
	import { gradingReport } from '$lib/stores.js';

	let mounted = $state(false);
	let isGrading = $state(false);
	let errorMsg = $state('');

	let essayText = $state('');
	let promptText = $state('');
	let charCount = $derived(essayText.length);

	// Default criteria to display so it's not empty
	let criteriaList = $state([
		{
			id: 'default-1',
			name: 'Thesis',
			description: 'Clear, arguable claim that responds to the prompt',
			weight: 1,
			possible_points: 20
		},
		{
			id: 'default-2',
			name: 'Evidence',
			description: 'Relevant sources cited and integrated properly',
			weight: 1,
			possible_points: 30
		},
		{
			id: 'default-3',
			name: 'Analysis',
			description: 'Depth of interpretation and connection to thesis',
			weight: 1,
			possible_points: 30
		},
		{
			id: 'default-4',
			name: 'Style & Mechanics',
			description: 'Tone, clarity, grammar, and spelling',
			weight: 1,
			possible_points: 20
		}
	]);

	onMount(() => {
		mounted = true;
	});

	let canSubmit = $derived(
		essayText.trim().length > 50 &&
			criteriaList.length > 0 &&
			criteriaList.every((c) => c.name.trim() !== '')
	);

	async function handleGrade() {
		isGrading = true;
		errorMsg = '';
		try {
			const API_URL = '/api/grade'; 

			const payload = {
				question: promptText,
				essay: essayText,
				rubric: {
					rubric_type: 'custom',
					scoring_type: 'points',
					criteria_list: criteriaList
				}
			};

			const response = await fetch(API_URL, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(payload)
			});

			if (!response.ok) {
				let customMsg = `API returned ${response.status}: ${response.statusText}`;
				try {
					const errBody = await response.json();
					if (errBody.details) {
						try {
							const parsed = JSON.parse(errBody.details);
							if (parsed.detail) {
								customMsg = parsed.detail;
							} else {
								customMsg = errBody.details;
							}
						} catch (e) {
							customMsg = errBody.details;
						}
					} else if (errBody.error) {
						customMsg = errBody.error;
					}
				} catch (e) {
					// silently ignore parsing error and keep default
				}
				throw new Error(customMsg);
			}

			const data = await response.json();
			
			// Store the returned results
			gradingReport.set(data);
			
			// Navigate to results page
			goto('/results');
		} catch (err) {
			console.error('Error grading essay:', err);
			errorMsg = err instanceof Error ? err.message : 'An unknown error occurred';
		} finally {
			isGrading = false;
		}
	}
</script>

<div class="root" class:mounted>
	<div class="bg-grid" aria-hidden="true"></div>
	<div class="bg-glow" aria-hidden="true"></div>

	<main class="page" class:mounted>
		<div class="page-header">
			<div class="hero-label">New Submission</div>
			<h1>Grade an essay</h1>
			<p class="page-sub">Fill in the details below, then submit for AI-powered feedback.</p>
		</div>

		<div class="form-layout">
			<!-- Rubric section -->
			<section class="rubric-section">
				<section class="section-card">
					<div class="section-head">
						<span class="section-num">01</span>
						<div>
							<h2>Rubric</h2>
							<p class="section-desc">Define the criteria for evaluating this essay.</p>
						</div>
					</div>

					<RubricBuilder bind:criteriaList />
				</section>
			</section>
			

			<!-- Prompt section -->
			<section class="prompt-section">
				<!-- Essay Prompt -->
				<section class="section-card">
					<div class="section-head">
						<span class="section-num">02</span>
						<div>
							<h2>Essay Prompt</h2>
							<p class="section-desc">
								Optional — helps the AI assess relevance and argumentation.
							</p>
						</div>
					</div>
					<textarea
						class="prompt-textarea"
						placeholder="Paste or type the essay prompt here…"
						rows="3"
						oninput={(e) => (promptText = e.target.value)}
					></textarea>
				</section>
			</section>

			<section class="essay-section">
				<!-- Essay Body -->
				<section class="section-card">
					<div class="section-head">
						<span class="section-num">03</span>
						<div>
							<h2>Essay</h2>
							<p class="section-desc">Paste the full essay text below.</p>
						</div>
					</div>
					<div class="essay-box" class:has-content={essayText.length > 0}>
						<textarea
							placeholder="Start typing or paste an essay here…"
							rows="12"
							oninput={(e) => (essayText = e.target.value)}
						></textarea>
						<div class="essay-footer">
							<span class="char-count">{charCount} characters</span>
							{#if charCount < 50 && charCount > 0}
								<span class="char-warn">Too short to grade</span>
							{/if}
						</div>
					</div>
				</section>
			</section>

			<section class="submit-section">
				{#if errorMsg}
					<div class="error-banner">{errorMsg}</div>
				{/if}
				<button class="submit-btn" disabled={!canSubmit || isGrading} onclick={handleGrade}>
					{#if isGrading}
						Grading...
					{:else if canSubmit}
						Grade this essay →
					{:else}
						Complete all fields to grade
					{/if}
				</button>
			</section>
		</div>
	</main>
</div>

<style>
	.root {
		min-height: 100vh;
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
	h1 {
		font-family: var(--font-display);
		font-size: clamp(2rem, 4vw, 3rem);
		line-height: 1.1;
		margin-bottom: 0.5rem;
	}
	.page-sub {
		color: var(--ink-muted);
		font-size: 0.95rem;
	}

	.form-layout {
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
	}

	.section-card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 12px;
		padding: 1.5rem;
	}
	.section-head {
		display: flex;
		align-items: flex-start;
		gap: 1rem;
		margin-bottom: 1.25rem;
	}
	.section-num {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		color: var(--accent);
		letter-spacing: 0.08em;
		padding-top: 2px;
		flex-shrink: 0;
	}
	.section-head h2 {
		font-family: var(--font-display);
		font-size: 1.1rem;
		margin-bottom: 0.2rem;
	}
	.section-desc {
		font-size: 0.8rem;
		color: var(--ink-muted);
	}

	.prompt-textarea {
		width: 100%;
		padding: 0.75rem 1rem;
		background: var(--surface-2);
		border: 1px solid var(--border);
		border-radius: 8px;
		color: var(--ink);
		font-family: var(--font-sans);
		font-size: 0.9rem;
		line-height: 1.6;
		resize: vertical;
		outline: none;
		caret-color: var(--accent);
		transition: border-color 0.2s;
	}
	.prompt-textarea:focus {
		border-color: rgba(200, 245, 90, 0.3);
	}
	.prompt-textarea::placeholder {
		color: var(--ink-muted);
	}

	.essay-box {
		background: var(--surface-2);
		border: 1px solid var(--border);
		border-radius: 8px;
		overflow: hidden;
		transition: border-color 0.2s;
	}
	.essay-box:focus-within {
		border-color: rgba(200, 245, 90, 0.3);
	}
	.essay-box textarea {
		width: 100%;
		padding: 1rem;
		background: transparent;
		border: none;
		outline: none;
		color: var(--ink);
		font-family: var(--font-sans);
		font-size: 0.95rem;
		line-height: 1.65;
		resize: vertical;
		caret-color: var(--accent);
	}
	.essay-box textarea::placeholder {
		color: var(--ink-muted);
	}
	.essay-footer {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.5rem 1rem;
		border-top: 1px solid var(--border);
	}
	.char-count {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		color: var(--ink-muted);
	}
	.char-warn {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		color: #e8a04a;
	}


	.submit-btn {
		width: 100%;
		padding: 0.75rem 1rem;
		margin-top: 0.25rem;
		background: var(--accent);
		color: #0d0f0e;
		border: none;
		border-radius: 8px;
		font-family: var(--font-sans);
		font-size: 0.9rem;
		font-weight: 500;
		cursor: pointer;
		transition:
			background 0.2s,
			opacity 0.2s;
	}
	.submit-btn:hover:not(:disabled) {
		background: var(--accent-dim);
	}
	.submit-btn:disabled {
		opacity: 0.35;
		cursor: not-allowed;
	}

	.error-banner {
		background: rgba(232, 160, 74, 0.1);
		color: #e8a04a;
		border: 1px solid rgba(232, 160, 74, 0.3);
		padding: 0.75rem 1rem;
		border-radius: 8px;
		margin-bottom: 1rem;
		font-family: var(--font-sans);
		font-size: 0.9rem;
	}
</style>
