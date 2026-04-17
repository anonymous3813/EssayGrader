import { writable } from 'svelte/store';

// Store for holding the resultant grading report
export const gradingReport = writable<any>(null);
