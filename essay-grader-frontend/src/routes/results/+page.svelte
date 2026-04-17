<script lang="ts">
	import { onMount } from 'svelte';
	import { gradingReport } from '$lib/stores.js';
	import { goto } from '$app/navigation';

	let mounted = $state(false);

	onMount(() => {
		mounted = true;
		if (!$gradingReport) {
			goto('/grade');
		}
	});

	let percentage = $derived(
		$gradingReport ? ($gradingReport.overall_score / $gradingReport.total_possible_score) * 100 : 0
	);
</script>

<div class="root" class:mounted>
	<div class="bg-grid" aria-hidden="true"></div>
	<div class="bg-glow" aria-hidden="true"></div>

	<main class="page" class:mounted>
		<div class="page-header">
			<a href="/grade" class="back-link">← Back to Editor</a>
			<div class="hero-label">Analysis Complete</div>
			<h1>Grading Report</h1>
		</div>

		{#if $gradingReport}
			{@const report = $gradingReport}
			<!-- Score Overview -->
			<section class="score-card">
			<div class="score-info">
				<h2>Overall Score</h2>
				<p class="feedback-summary">{report.final_feedback}</p>
			</div>
			<div class="score-display">
				<div class="score-circle">
					<svg viewBox="0 0 36 36" class="circular-chart">
						<path
							class="circle-bg"
							d="M18 2.0845
                           a 15.9155 15.9155 0 0 1 0 31.831
                           a 15.9155 15.9155 0 0 1 0 -31.831"
						/>
						<path
							class="circle"
							stroke-dasharray="{percentage}, 100"
							d="M18 2.0845
                           a 15.9155 15.9155 0 0 1 0 31.831
                           a 15.9155 15.9155 0 0 1 0 -31.831"
						/>
					</svg>
					<div class="score-text">
						<span class="score-num">{report.overall_score}</span>
						<span class="score-denom">/ {report.total_possible_score}</span>
					</div>
				</div>
			</div>
		</section>

		<!-- High-level feedback -->
		<div class="feedback-columns">
			<!-- Strengths -->
			<div class="feedback-panel strengths-panel">
				<div class="panel-header">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="20"
						height="20"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<path d="M12 2v20"></path>
						<path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
					</svg>
					<h3>Key Strengths</h3>
				</div>
				<ul class="feedback-list">
					{#each report.strengths as strength}
						<li>
							<span class="li-icon success">
								<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
									<polyline points="20 6 9 17 4 12"></polyline>
								</svg>
							</span>
							{strength}
						</li>
					{/each}
				</ul>
			</div>

			<!-- Areas for Improvement -->
			<div class="feedback-panel areas-panel">
				<div class="panel-header">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="20"
						height="20"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<circle cx="12" cy="12" r="10"></circle>
						<line x1="12" y1="8" x2="12" y2="12"></line>
						<line x1="12" y1="16" x2="12.01" y2="16"></line>
					</svg>
					<h3>Areas for Improvement</h3>
				</div>
				<ul class="feedback-list">
					{#each report.areas_for_improvement as area}
						<li>
							<span class="li-icon warning">
								<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
									<line x1="5" y1="12" x2="19" y2="12"></line>
									<polyline points="12 5 19 12 12 19"></polyline>
								</svg>
							</span>
							{area}
						</li>
					{/each}
				</ul>
			</div>
		</div>

		<!-- Detailed Criteria Breakdown -->
		<div class="detailed-breakdown">
			<h2 class="section-title">Rubric Breakdown</h2>
			<div class="criteria-list">
				{#each report.criteria_breakdown as crit}
					<div class="criterion-card">
						<div class="crit-header">
							<div class="crit-title">
								<h4>{crit.criteria_name}</h4>
							</div>
							<div class="crit-score-badge">
								{#if report.scoring_type === 'band'}
									Band {crit.band_score}
								{:else}
									<span class="actual">{crit.actual_score}</span>
									<span class="possible">/ {crit.possible_score}</span>
								{/if}
							</div>
						</div>

						<p class="crit-reasoning">{crit.reasoning}</p>

						{#if crit.strengths.length > 0 || crit.weaknesses.length > 0}
							<div class="crit-details">
								{#if crit.strengths.length > 0}
									<div class="detail-col">
										<h5 class="success-text">Strengths</h5>
										<ul>
											{#each crit.strengths as s}
												<li>{s}</li>
											{/each}
										</ul>
									</div>
								{/if}
								{#if crit.weaknesses.length > 0}
									<div class="detail-col">
										<h5 class="warning-text">Weaknesses</h5>
										<ul>
											{#each crit.weaknesses as w}
												<li>{w}</li>
											{/each}
										</ul>
									</div>
								{/if}
							</div>
						{/if}
					</div>
				{/each}
			</div>
		</div>
		{/if}
	</main>
</div>

<style>
	.root {
		min-height: 100vh;
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
		top: -30%;
		right: -10%;
		width: 800px;
		height: 800px;
		pointer-events: none;
		z-index: 0;
		border-radius: 50%;
		background: radial-gradient(circle, rgba(200, 245, 90, 0.05) 0%, transparent 60%);
	}

	.page {
		position: relative;
		z-index: 5;
		max-width: 900px;
		margin: 0 auto;
		padding: 3rem 2rem;
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
		text-align: center;
	}
	.back-link {
		display: inline-block;
		color: var(--ink-muted);
		text-decoration: none;
		font-size: 0.9rem;
		margin-bottom: 1.5rem;
		transition: color 0.2s;
	}
	.back-link:hover {
		color: var(--accent);
	}
	.hero-label {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		color: var(--accent);
		letter-spacing: 0.12em;
		text-transform: uppercase;
		margin-bottom: 0.5rem;
	}
	h1 {
		font-family: var(--font-display);
		font-size: clamp(2rem, 4vw, 3rem);
		line-height: 1.1;
		margin-bottom: 0.5rem;
	}

	/* Score Card */
	.score-card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 16px;
		padding: 2.5rem;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 3rem;
		margin-bottom: 1.5rem;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
	}
	.score-info h2 {
		font-family: var(--font-display);
		font-size: 1.8rem;
		margin-bottom: 0.75rem;
	}
	.feedback-summary {
		color: var(--ink-muted);
		line-height: 1.6;
		font-size: 1rem;
	}
	.score-display {
		flex-shrink: 0;
	}
	.score-circle {
		position: relative;
		width: 140px;
		height: 140px;
	}
	.circular-chart {
		display: block;
		margin: 0 auto;
		max-width: 100%;
		max-height: 250px;
	}
	.circle-bg {
		fill: none;
		stroke: rgba(255, 255, 255, 0.05);
		stroke-width: 2.5;
	}
	.circle {
		fill: none;
		stroke-width: 2.5;
		stroke-linecap: round;
		stroke: var(--accent);
		animation: progress 1.5s ease-out forwards;
	}
	@keyframes progress {
		0% {
			stroke-dasharray: 0 100;
		}
	}
	.score-text {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		text-align: center;
		display: flex;
		flex-direction: column;
	}
	.score-num {
		font-family: var(--font-display);
		font-size: 2.5rem;
		line-height: 1;
		color: var(--ink);
	}
	.score-denom {
		font-family: var(--font-mono);
		font-size: 0.8rem;
		color: var(--ink-muted);
		margin-top: 0.2rem;
	}

	/* Feedback Columns */
	.feedback-columns {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
		margin-bottom: 3rem;
	}
	.feedback-panel {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 12px;
		padding: 1.5rem;
	}
	.panel-header {
		display: flex;
		align-items: center;
		gap: 0.75rem;
		margin-bottom: 1.25rem;
	}
	.strengths-panel .panel-header svg {
		color: var(--accent);
	}
	.areas-panel .panel-header svg {
		color: #e8a04a; /* warning orange */
	}
	.panel-header h3 {
		font-family: var(--font-display);
		font-size: 1.2rem;
	}

	.feedback-list {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.8rem;
	}
	.feedback-list li {
		display: flex;
		align-items: flex-start;
		gap: 0.75rem;
		font-size: 0.95rem;
		line-height: 1.5;
		color: var(--ink-muted);
	}
	.li-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 20px;
		height: 20px;
		flex-shrink: 0;
		margin-top: 0.15rem;
		border-radius: 4px;
	}
	.li-icon.success {
		background: rgba(200, 245, 90, 0.1);
		color: var(--accent);
	}
	.li-icon.warning {
		background: rgba(232, 160, 74, 0.1);
		color: #e8a04a;
	}
	.li-icon svg {
		width: 12px;
		height: 12px;
	}

	/* Detailed Breakdown */
	.section-title {
		font-family: var(--font-display);
		font-size: 1.8rem;
		margin-bottom: 1.5rem;
		text-align: center;
	}
	.criteria-list {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	.criterion-card {
		background: var(--surface);
		border: 1px solid var(--border);
		border-radius: 12px;
		padding: 1.5rem;
		transition: border-color 0.2s;
	}
	.criterion-card:hover {
		border-color: rgba(255, 255, 255, 0.15);
	}
	.crit-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1rem;
	}
	.crit-title h4 {
		font-family: var(--font-sans);
		font-size: 1.1rem;
		font-weight: 500;
	}
	.crit-score-badge {
		background: rgba(255, 255, 255, 0.05);
		padding: 0.4rem 0.8rem;
		border-radius: 20px;
		font-family: var(--font-mono);
		font-size: 0.85rem;
	}
	.crit-score-badge .actual {
		color: var(--accent);
		font-weight: 500;
	}
	.crit-score-badge .possible {
		color: var(--ink-muted);
	}
	.crit-reasoning {
		font-size: 0.95rem;
		line-height: 1.6;
		color: var(--ink-muted);
		margin-bottom: 1.5rem;
	}
	.crit-details {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 1.5rem;
		padding-top: 1.25rem;
		border-top: 1px solid var(--border);
	}
	.detail-col h5 {
		font-family: var(--font-mono);
		font-size: 0.72rem;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		margin-bottom: 0.75rem;
	}
	.success-text {
		color: var(--accent);
	}
	.warning-text {
		color: #e8a04a;
	}
	.detail-col ul {
		list-style: none;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}
	.detail-col ul li {
		position: relative;
		padding-left: 1rem;
		font-size: 0.9rem;
		color: var(--ink-muted);
		line-height: 1.4;
	}
	.detail-col ul li::before {
		content: '•';
		position: absolute;
		left: 0;
		color: currentColor;
		opacity: 0.5;
	}

	@media (max-width: 768px) {
		.score-card {
			flex-direction: column;
			gap: 1.5rem;
			text-align: center;
		}
		.feedback-columns {
			grid-template-columns: 1fr;
		}
		.crit-details {
			grid-template-columns: 1fr;
		}
	}
</style>
