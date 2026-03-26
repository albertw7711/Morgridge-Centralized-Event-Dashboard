export interface EventInfo {
	id: number;
	eventTitle: string;
	eventHost: string;
	eventLocation: string;
	eventDay: string;
	eventStartTime: string;
	eventDuration: string;
	eventDescription: string;
	food: boolean;
	media: string[];
}

function relativeDate(offsetDays: number): string {
	const date = new Date();
	date.setDate(date.getDate() + offsetDays);
	return `${date.getMonth() + 1}/${date.getDate()}/${date.getFullYear()}`;
}

const today = relativeDate(0);
const tomorrow = relativeDate(1);
const in2Days = relativeDate(2);
const in3Days = relativeDate(3);
const in5Days = relativeDate(5);
const in7Days = relativeDate(7);

export const mockEvents: EventInfo[] = [
	// Today (+0)
	{
		id: 1,
		eventTitle: 'WebTalks: SvelteKit & GitHub Actions',
		eventHost: 'WebLabs',
		eventLocation: 'Morgridge Hall Rm. 2556',
		eventDay: today,
		eventStartTime: '6:00 PM',
		eventDuration: '1 hour',
		eventDescription:
			"WebLabs is hosting a workshop with a frontend engineer from Fetch on publishing a website using SvelteKit and GitHub Actions. Whether you're a frontend warrior or just interested in standing up a portfolio site for your resume, this workshop will have something for everyone! Like usual for WebLabs, this event will feature pizza 🍕",
		food: true,
		media: ['https://i.redd.it/2nj600aenfnf1.png']
	},
	{
		id: 2,
		eventTitle: 'CS Department Coffee Hour',
		eventHost: 'UW–Madison CS Department',
		eventLocation: 'Morgridge Hall Atrium',
		eventDay: today,
		eventStartTime: '2:00 PM',
		eventDuration: '1 hour',
		eventDescription:
			'Drop by the atrium for a casual coffee hour with CS faculty, researchers, and fellow students. A great chance to hear about ongoing projects and ask questions in a relaxed setting. Light refreshments will be provided.',
		food: true,
		media: []
	},
	{
		id: 3,
		eventTitle: 'Craft Night Social',
		eventHost: 'Girls Who Code — Madison Chapter',
		eventLocation: 'Morgridge Hall Student Org Lounge (2nd floor)',
		eventDay: today,
		eventStartTime: '7:30 PM',
		eventDuration: '1.5 hours',
		eventDescription:
			'Join us for a break from studying to decorate our club locker and meet other fellow members! We will have arts/craft supplies 🖌️✂️ for you to make decorations. We hope to see you there!!',
		food: false,
		media: ['https://www.mamp.one/wp-content/uploads/2024/09/image-resources2.jpg']
	},
	// Tomorrow (+1)
	{
		id: 4,
		eventTitle: 'UPL Research Talk: Getting into Undergrad Research',
		eventHost: 'UPL',
		eventLocation: 'Morgridge Hall Rm. 1524',
		eventDay: tomorrow,
		eventStartTime: '6:00 PM',
		eventDuration: '1 hour',
		eventDescription:
			"The UPL is hosting a talk on getting into research as an undergrad for the first time! We'll be sharing what we've personally learned about reaching out to labs, finding advisors, and making the most of your time once you're in. Whether you're interested in research for grad school, industry, or pure curiosity, feel free to stop by. Food will be provided 🍕",
		food: true,
		media: [
			'https://cdn.discordapp.com/attachments/1423716763711045705/1473462011881848842/flyer.jpg?ex=69a180af&is=69a02f2f&hm=48183abc7d49de6070f133fa6ca6c1f18490fe424c85be3624f3b840ae8c2347&'
		]
	},
	{
		id: 5,
		eventTitle: 'Spring Hackathon Kickoff',
		eventHost: 'ACM @ UW–Madison',
		eventLocation: 'Morgridge Hall Rm. 3810',
		eventDay: tomorrow,
		eventStartTime: '5:00 PM',
		eventDuration: '2 hours',
		eventDescription:
			'Kick off the ACM Spring Hackathon with a team-matching session and project brainstorm! Come meet potential teammates, hear about the theme, and get hyped for the weekend. Dinner will be served 🍕',
		food: true,
		media: []
	},
	// This Week (+2)
	{
		id: 6,
		eventTitle: 'Resume & LinkedIn Workshop',
		eventHost: 'CS Career Center',
		eventLocation: 'Morgridge Hall Rm. 2260',
		eventDay: in2Days,
		eventStartTime: '3:00 PM',
		eventDuration: '1.5 hours',
		eventDescription:
			"Bring your resume and get personalized feedback from career advisors and industry volunteers. We'll also cover LinkedIn optimization, networking tips, and how to tell your story as a CS student heading into internship and new-grad recruiting.",
		food: false,
		media: []
	},
	{
		id: 7,
		eventTitle: 'CDIS Game Night',
		eventHost: 'CDIS Student Organization',
		eventLocation: 'Morgridge Hall Student Org Lounge (2nd floor)',
		eventDay: in2Days,
		eventStartTime: '7:00 PM',
		eventDuration: '2 hours',
		eventDescription:
			'Wind down the week with board games, card games, and video games hosted by CDIS student orgs. All skill levels and majors welcome — just come ready to have fun! Snacks will be provided 🍕',
		food: true,
		media: []
	},
	// This Week (+3)
	{
		id: 8,
		eventTitle: 'ACM Spring Hackathon Day 1',
		eventHost: 'ACM @ UW–Madison',
		eventLocation: 'Morgridge Hall Rm. 3810',
		eventDay: in3Days,
		eventStartTime: '9:00 AM',
		eventDuration: '10 hours',
		eventDescription:
			'The full-day build session for the ACM Spring Hackathon. Teams work on their projects and mentors will be on hand to help with technical challenges. Meals and snacks provided throughout the day 🍕',
		food: true,
		media: []
	},
	// Next Week (+5)
	{
		id: 9,
		eventTitle: 'Intro to Machine Learning',
		eventHost: 'UW–Madison ML Club',
		eventLocation: 'Morgridge Hall Rm. 1310',
		eventDay: in5Days,
		eventStartTime: '6:00 PM',
		eventDuration: '1 hour',
		eventDescription:
			'A beginner-friendly overview of machine learning concepts including supervised learning, neural networks, and common frameworks like PyTorch. No prior ML experience needed — just bring your curiosity!',
		food: false,
		media: []
	},
	// Next Week (+7)
	{
		id: 10,
		eventTitle: 'Open Source Contribution Workshop',
		eventHost: 'GitHub Campus Experts',
		eventLocation: 'Morgridge Hall Rm. 2556',
		eventDay: in7Days,
		eventStartTime: '5:30 PM',
		eventDuration: '1.5 hours',
		eventDescription:
			"Learn how to make your first open source contribution! We'll walk through finding good first issues, understanding contribution guidelines, writing clean pull requests, and engaging with maintainers. Bring your laptop and a project you'd like to contribute to.",
		food: false,
		media: []
	}
];
