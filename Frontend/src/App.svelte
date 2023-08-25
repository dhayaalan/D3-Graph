<script>
	import { select } from 'd3-selection';
	import {
		forceSimulation,
		forceManyBody,
		forceCenter,
		forceLink,
	} from 'd3-force';
	import { onMount } from 'svelte';
	import { drag } from 'd3-drag';
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

	let selectedNode = null;

	const handleNodeClick = (node) => {
		selectedNode = node;
	};

	const width = window.innerWidth;
	const height = window.innerHeight;

	onMount(() => {
		let svg = select('svg').attr('width', width).attr('height', height);

		const simulation = forceSimulation(nodes)
			.force('charge', forceManyBody().strength(-20))
			.force('center', forceCenter(width / 2, height / 2));

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

		simulation.nodes(nodes).on('tick', () => {
			nodeElements.attr('cx', (node) => node.x).attr('cy', (node) => node.y);
			textElements.attr('x', (node) => node.x).attr('y', (node) => node.y);
		});

		simulation.force(
			'link',
			forceLink()
				.id((link) => link.id)
				.strength((link) => link.strength)
		);

		const linkElements = svg
			.append('g')
			.selectAll('line')
			.data(links)
			.enter()
			.append('line')
			.attr('stroke-width', 1)
			.attr('stroke', '#E5E5E5');

		linkElements
			.attr('x1', (link) => link.source.x)
			.attr('y1', (link) => link.source.y)
			.attr('x2', (link) => link.target.x)
			.attr('y2', (link) => link.target.y);

		// simulation.force('link').link(links);

		// simulation.links(links).on('click', () => {
		// 	linkElements
		// 		.attr('x1', (link) => link.source.x)
		// 		.attr('y1', (link) => link.source.y)
		// 		.attr('x2', (link) => link.target.x)
		// 		.attr('y2', (link) => link.target.y);
		// });

		const dragDrop = drag()
			.on('start', (node) => {
				node.fx = node.x;
				node.fy = node.y;
			})
			.on('drag', (node) => {
				simulation.alphaTarget(0.7).restart();
				node.fx = node.x;
				node.fy = node.y;
			})
			.on('end', (node) => {
				if (!node.active) {
					simulation.alphaTarget(0);
				}
				node.fx = null;
				node.fy = null;
			});

		nodeElements.call(dragDrop);

		// function getNeighbors(node) {
		// 	return links.reduce(
		// 		(neighbors, link) => {
		// 			if (link.target.id === node.id) {
		// 				neighbors.push(link.source.id);
		// 			} else if (link.source.id === node.id) {
		// 				neighbors.push(link.target.id);
		// 			}
		// 			return neighbors;
		// 		},
		// 		[node.id]
		// 	);
		// }
		// function isNeighborLink(node, link) {
		// 	return link.target.id === node.id || link.source.id === node.id;
		// }

		// function getNodeColor(node, neighbors) {
		// 	if (neighbors.indexOf(node.id)) {
		// 		return node.level === 1 ? 'blue' : 'green';
		// 	}
		// 	return node.level === 1 ? 'red' : 'gray';
		// }
		// function getTextColor(node, neighbors) {
		// 	return neighbors.indexOf(node.id) ? 'green' : 'black';
		// }
		// function getLinkColor(node, link) {
		// 	return isNeighborLink(node, link) ? 'green' : '#E5E5E5';
		// }

		// function selectNode(selectedNode) {
		// 	const neighbors = getNeighbors(selectedNode);
		// 	nodeElements.attr('fill', (node) => getNodeColor(node, neighbors));
		// 	textElements.attr('fill', (node) => getTextColor(node, neighbors));
		// 	linkElements.attr('stroke', (link) => getLinkColor(selectedNode, link));
		// }

		// nodeElements.on('click', selectNode);
	});
</script>

<form class="row g-3">
	<div class="col-md-3">
		<input
			type="email"
			class="form-control"
			id="inputEmail4"
			placeholder="Source"
		/>
	</div>
	<div class="col-md-3">
		<input
			type="email"
			class="form-control"
			id="inputEmail4"
			placeholder="Destination"
		/>
	</div>
	<div class="col">
		<button
			type="submit"
			class="btn btn-primary">Search</button
		>
	</div>
</form>

<svg on:click={() => (selectedNode = null)} />

{#if selectedNode}
	<div class="node-details">
		<h3>{selectedNode.label}</h3>
		<!-- Display other details of the selected node -->
	</div>
{/if}

<style>
	.node-details {
		position: absolute;
		background: white;
	}
</style>
