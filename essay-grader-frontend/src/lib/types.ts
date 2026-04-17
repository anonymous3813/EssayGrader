export type ScoringType = 'points' | 'percentage' | string;

export interface RubricCriteria {
    id?: string;
    name: string;
    description: string;
    weight: number;
    possible_points: number;
}

export interface Rubric {
    rubric_type: string;
    scoring_type: ScoringType;
    criteria_list: RubricCriteria[];
}

export interface Input {
    question: string;
    essay: string;
    rubric: Rubric;
}

export interface TemplateOption extends Rubric {
    id: string;
    label: string;
    desc?: string;
    tags?: string[];
}

export const templatesOptions: TemplateOption[] = [
    {
        id: 'APUSH',
        label: 'APUSH LEQ',
        desc: 'Advanced Placement U.S. History Long Essay Question',
        tags: ['APUSH', 'History', 'LEQ'],
        rubric_type: 'APUSH',
        scoring_type: 'points',
        criteria_list: [
            {
                name: 'Thesis / Claim',
                description: 'Responds to the prompt with a historically defensible thesis or claim that establishes a clear line of reasoning. The thesis must directly answer the prompt and be located in the introduction or conclusion.',
                weight: 1,
                possible_points: 1
            },
            {
                name: 'Contextualization',
                description: "Describes a broader historical context relevant to the prompt. The response must explain relevant historical developments, events, or processes occurring before, during, or after the time period in the prompt. Vague and overgeneralized responses don't earn the point, although they can be broad and don't need to be super specific.",
                weight: 1,
                possible_points: 1
            },
            {
                name: 'Evidence',
                description: 'Uses specific and relevant historical evidence to address the prompt. 1 point: Provides specific examples of evidence relevant to the topic. 2 points: Supports an argument in response to the prompt using specific and relevant historical evidence.',
                weight: 1,
                possible_points: 2
            },
            {
                name: 'Analysis and Reasoning',
                description: 'Uses historical reasoning such as comparison, causation, or continuity and change to structure an argument that addresses the prompt. 1 point: Uses historical reasoning to frame the argument. 2 points: Demonstrates a complex understanding of the historical development through sophisticated argumentation, qualification, or multiple perspectives.',
                weight: 1,
                possible_points: 2
            }
        ]
    },
    {
        id: 'IELTS',
        label: 'IELTS Writing Task 2',
        desc: 'Standardized assessment rubric used for IELTS writing tasks.',
        tags: ['IELTS', 'Standardized'],
        rubric_type: 'IELTS',
        scoring_type: 'band',
        criteria_list: [
            {
                name: 'Task Response',
                description: 'Addresses all parts of the prompt, presents a clear position, and supports ideas with relevant arguments.',
                weight: 1.0,
                possible_points: 9
            },
            {
                name: 'Coherence and Cohesion',
                description: 'Logical organization, clear progression, effective paragraphing.',
                weight: 1.0,
                possible_points: 9
            },
            {
                name: 'Lexical Resource',
                description: 'Vocabulary range, precision, and accuracy.',
                weight: 1.0,
                possible_points: 9
            },
            {
                name: 'Grammatical Range and Accuracy',
                description: 'Grammar variety and accuracy.',
                weight: 1.0,
                possible_points: 9
            }
        ]
    }
];