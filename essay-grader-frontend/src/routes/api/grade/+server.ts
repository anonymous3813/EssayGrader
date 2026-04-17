import { json } from '@sveltejs/kit';
import { BASE_BACKEND_URL } from '$env/static/private';

export async function POST({ request }) {
	try {
		const payload = await request.json();

		const apiUrl = `${BASE_BACKEND_URL}/grader/grade`;

		const response = await fetch(apiUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(payload)
		});

		if (!response.ok) {
			const errorText = await response.text();
			console.error(`Backend error (${response.status}):`, errorText);
			return new Response(JSON.stringify({ error: `Backend API failed: ${response.statusText}`, details: errorText }), {
				status: response.status,
				headers: { 'Content-Type': 'application/json' }
			});
		}

		const data = await response.json();
		return json(data);
	} catch (error: any) {
		console.error('Error proxying request to backend:', error);
		return new Response(JSON.stringify({ error: 'Internal Server Error proxying request', details: error.message }), {
			status: 500,
			headers: { 'Content-Type': 'application/json' }
		});
	}
}
