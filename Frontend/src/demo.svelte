<script>
	import d3 from 'd3';
	let nodes = [
		{ id: 'mammal', group: 0, label: 'Mammals', level: 1 },
		{ id: 'dog', group: 0, label: 'Dogs', level: 2 },
		{ id: 'cat', group: 0, label: 'Cats', level: 2 },
		{ id: 'fox', group: 0, label: 'Foxes', level: 2 },
		{ id: 'elk', group: 0, label: 'Elk', level: 2 },
		{ id: 'insect', group: 1, label: 'Insects', level: 1 },
		{ id: 'ant', group: 1, label: 'Ants', level: 2 },
		{ id: 'bee', group: 1, label: 'Bees', level: 2 },
		{ id: 'fish', group: 2, label: 'Fish', level: 1 },
		{ id: 'carp', group: 2, label: 'Carp', level: 2 },
		{ id: 'pike', group: 2, label: 'Pikes', level: 2 },
	];

	let links = [
		{ target: 'mammal', source: 'dog', strength: 0.7 },
		{ target: 'mammal', source: 'cat', strength: 0.7 },
		{ target: 'mammal', source: 'fox', strength: 0.7 },
		{ target: 'mammal', source: 'elk', strength: 0.7 },
		{ target: 'insect', source: 'ant', strength: 0.7 },
		{ target: 'insect', source: 'bee', strength: 0.7 },
		{ target: 'fish', source: 'carp', strength: 0.7 },
		{ target: 'fish', source: 'pike', strength: 0.7 },
		{ target: 'cat', source: 'elk', strength: 0.1 },
		{ target: 'carp', source: 'ant', strength: 0.1 },
		{ target: 'elk', source: 'bee', strength: 0.1 },
		{ target: 'dog', source: 'cat', strength: 0.1 },
		{ target: 'fox', source: 'ant', strength: 0.1 },
		{ target: 'pike', source: 'dog', strength: 0.1 },
	];

	const width = window.innerWidth;
	const height = window.innerHeight;
	const svg = d3.select('svg').attr('width', width).attr('height', height);

	const simulation = d3
		.forceSimulation()
		.force('charge', d3.forceManyBody().strength(-20))
		.force('center', d3.forceCenter(width / 2, height / 2));

	function getNodeColor(node) {
		return node.level === 1 ? 'red' : 'gray';
	}
	const nodeElements = svg
		.append('g')
		.selectAll('circle')
		.data(nodes)
		.enter()
		.append('circle')
		.attr('r', 10)
		.attr('fill', getNodeColor);
	const textElements = svg
		.append('g')
		.selectAll('text')
		.data(nodes)
		.enter()
		.append('text')
		.text((node) => node.label)
		.attr('font-size', 15)
		.attr('dx', 15)
		.attr('dy', 4);
</script>
