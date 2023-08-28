<script>
	import axios from 'axios';
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
		// {
		// 	group: 0,
		// 	id: 'mammal',
		// 	label: 'Mammals',
		// 	level: 1,
		// },
		// {
		// 	group: 0,
		// 	id: 'mammal',
		// 	label: 'Mammals',
		// 	level: 1,
		// },
	];

	let links = [];

	let selectedNode = null;

	const handleNodeClick = (node) => {
		selectedNode = node;
	};

	const dataNodes = async (nodes) => {
		const res = await axios({
			method: 'get',
			credential: 'include',
			url: 'http://127.0.0.1:4000/get_nodes',
		});
		console.log(res.data, 'result');
		nodes = res.data;
		console.log(nodes, 'nodes');
	};

	const width = 500;
	const height = 500;

	onMount(() => {
		// dataNodes(nodes);
		// console.timeLog(dataNodes(nodes))
		

		
		let list = select('svg').attr('width', width).attr('height', height);
		// console.log('list',list);

		// console.log(nodes, 'nodes');
		const simulation = forceSimulation(nodes)
			.force('charge', forceManyBody().strength(-20))
			.force('center', forceCenter(width / 2, height / 2));

          // console.log(nodes, 'simulation');

		function getNodeColor(node) {
			return node.level === 1 ? 'red' : 'gray';
		}
		const nodeElements = list
			.append('g')
			.selectAll('circle')
			.data(nodes)
			.enter()
			.append('circle')
			.attr('r', 10)
			.attr('fill', getNodeColor);
		const textElements = list
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

		const linkElements = list
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

<!-- <form class="row g-3">
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
</form> -->

<svg />

<!-- 
{#if selectedNode}
	<div class="node-details">
		<h3>{selectedNode.label}</h3>
		 Display other details of the selected node -->
<!-- </div> -->
<!-- {/if}  -->

<!-- <style>
	.node-details {
		position: absolute;
		background: white;
	}
</style> -->
