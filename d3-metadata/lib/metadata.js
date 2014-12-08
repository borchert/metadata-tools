$(function() {
	/* ------------------------------------

	Expand/collapse button functionality

	---------------------------------------*/
	
	$("#expandAll").on('click', function () {
		console.log('Clicked expand all');

		function expandAll(d) {
		    console.log("Expanding");
			if (d._children) {
			console.log("Expanding children");
				d._children.forEach(expandAll);
				toggle(d);
				update(root);
			}
		}
		
		// Toggle children.
		function toggle(d) {
		  //console.log(d.children);
		  console.log(d._children);
			if (d.children) {
				console.log("!!!!");
				d._children = d.children;
				d.children = null;
			} else {
			console.log("....");
				d.children = d._children;
				d._children = null;
			}
		}
		//console.log(root);
		if (root.children){
		  //close tree
		  console.log("Closing tree");
		  toggle(root);
		  //console.log(root._children);
		  update(root);
		  console.log(root._children);
		  root._children.forEach(expandAll);
		  update(root);
		  
		  }
		else{
		  console.log("Hidden children");
		  /*root._children.forEach(expandAll); 
		  update(root);*/
		  };
		//toggle(root.children);

		//root._children.forEach(expandAll); 
		//update(root);
	});


	$("#collapseAll").on('click', function (e) {
	
	    if(e.ctrlKey){
          console.log('ctrl');
		  }

		/*function moveChildren(node) {
		if(node.children) {
			node.children.forEach(function(c) { moveChildren(c); });
			node._children = node.children;
			node.children = null;
		}
	}
	moveChildren(root);*/
		toggle(root);
		update(root);
	});

	/* ------------------------------------

	Search functionality

	---------------------------------------*/

	//Variable to hold autocomplete options
	var keys;

	//Load US States as options from CSV - but this can also be created dynamically
	d3.csv("iso.csv", function (csv) {
		keys = csv;
		start();
	});


	//Call back for when user selects an option
	function onSelect(d) {

		var node = d3.selectAll("[id='" + d.name +"']")
		
		node.selectAll("circle")
		  .style("fill", function (d) { return '#ff0000'; })
		  .style("stroke", function (d) { return '#000'; })
		
		node.selectAll("text")
		  .style("font-size", function (d) { return '20'; })
		  .style("fill", function (d) { return '#ff0000'; })
		 
	}

	//Setup and render the autocomplete
	function start() {
		var mc = autocomplete(document.getElementById('test'))
			.keys(keys)
			.dataField("name")
			.placeHolder("Search Metadata - Start typing here")
			.width(960)
			.height(500)
			.onSelected(onSelect)
			.render();
	}

	// Build name values
	nameArray = [];
	humanNameArray = [];

	function traverse(o) {
		for (i in o) {
			if (typeof (o[i]) == "object") {
				if (typeof o[i]["name"] != 'undefined') {
					if (name.indexOf(o[i]["name"]) == -1) {
						name = o[i]["name"];
						nameArray.push(name);

					}
					if (name.indexOf(o[i]["easyname"]) == -1) {
						name = o[i]["easyname"];
						humanNameArray.push(name);

					}

				}

				traverse(o[i]);
			}
		}
	}
	
	
	function mousedown() {
	  console.log("Mouse down");
  //if (!mousedown_node && !mousedown_link) {
    // allow panning if nothing is selected
    //vis.call(d3.behavior.zoom().on("zoom"), rescale);
    return;
  //}
}

// rescale g
function rescale() {
  trans=d3.event.translate;
  scale=d3.event.scale;

  vis.attr("transform",
      "translate(" + trans + ")"
      + " scale(" + scale + ")");
}


	/* ------------------------------------

	D3 set up

	---------------------------------------*/

	var m = [20, 120, 20, 120],
		w = 1480 - m[1] - m[3],
		h = 800 - m[0] - m[2],
		i = 0,
		root;

	var tree = d3.layout.tree()
		.size([h, w]);

	var diagonal = d3.svg.diagonal()
		.projection(function (d) {
		return [d.y, d.x];
	});

	var vis = d3.select("#body").append("svg:svg")
		.attr("width", w + m[1] + m[3])
		.attr("height", h + m[0] + m[2])
		.append("svg:g")
		  .on("mousedown", mousedown)
		.attr("transform", "translate(" + m[3] + "," + m[0] + ")");

	d3.json("iso.json", function (json) {
		root = json;
		root.x0 = h / 2;
		root.y0 = 0;

		function toggleAll(d) {
			if (d.children) {
				d.children.forEach(toggleAll);
				toggle(d);
			}
		}

		// Initialize the display to show a few nodes.
		root.children.forEach(toggleAll);
		//toggle(root.children[0]);
		//toggle(root.children[2].children[0]);
		update(root);
	});

	// Build list of nodes (name and human name)
	/*d3.json("iso.json", function (json) {
		console.log("Called Round 2");
		root = json;
		traverse(root);

	});*/

	/*function separation(a, b) {
	  return a.parent == b.parent ? 1 : 5;
	};*/

	function update(source) {
		var duration = d3.event && d3.event.altKey ? 5000 : 500;

		// Compute the new tree layout.
		var nodes = tree.nodes(root).reverse();

		// Normalize for fixed-depth.
		nodes.forEach(function (d) {
			d.y = d.depth * 120;
		});

		// Update the nodes…
		var node = vis.selectAll("g.node")
			.data(nodes, function (d) {
			return d.id || (d.id = ++i);
		});

		// Enter any new nodes at the parent's previous position.
		var nodeEnter = node.enter().append("svg:g")
			.attr("class", "node")
			.attr("id", function(d){ return d.name; })
			.attr("transform", function (d) {
			return "translate(" + source.y0 + "," + source.x0 + ")";
		})
			.on("click", function (d) {
			toggle(d);
			update(d);
		})
			.on("mouseover", function (d) {
			var g = d3.select(this); // The node
			// The class is used to remove the additional text later
			var info = g.append('text')
				.classed('info', true)
				.attr('x', -30)
				.attr('y', -10)
				.text(function (d) {
				return d.humanname;
			});
		})
			.on("mouseout", function () {
			// Remove the info text on mouse out.
			d3.select(this).select('text.info').remove();
		});

		nodeEnter.append("svg:circle")
			.attr("r", 1e-6)
			.style("fill", function (d) {
			return d._children ? "lightsteelblue" : "#fff";
		});

		nodeEnter.append("svg:text")
			.attr("x", function (d) {
			return d.children || d._children ? -10 : 10;
		})
			.attr("y", -10)
			.attr("dy", ".35em")
			.attr("text-anchor", function (d) {
			return d.children || d._children ? "end" : "start";
		})
			.text(function (d) {
			return d.name;
		})
			.style("fill-opacity", 1e-6);

		// Transition nodes to their new position.
		var nodeUpdate = node.transition()
			.duration(duration)
			.attr("transform", function (d) {
			return "translate(" + d.y + "," + d.x + ")";
		});

		nodeUpdate.select("circle")
			.attr("r", 4.5)
			.style("fill", function (d) {
			return d._children ? "lightsteelblue" : "#fff";
		});

		nodeUpdate.select("text")
			.style("fill-opacity", 1);

		// Transition exiting nodes to the parent's new position.
		var nodeExit = node.exit().transition()
			.duration(duration)
			.attr("transform", function (d) {
			return "translate(" + source.y + "," + source.x + ")";
		})
			.remove();

		nodeExit.select("circle")
			.attr("r", 1e-6);

		nodeExit.select("text")
			.style("fill-opacity", 1e-6);

		// Update the links…
		var link = vis.selectAll("path.link")
			.data(tree.links(nodes), function (d) {
			return d.target.id;
		});

		// Enter any new links at the parent's previous position.
		link.enter().insert("svg:path", "g")
			.attr("class", "link")
			.attr("d", function (d) {
			var o = {
				x: source.x0,
				y: source.y0
			};
			return diagonal({
				source: o,
				target: o
			});
		})
			.transition()
			.duration(duration)
			.attr("d", diagonal);

		// Transition links to their new position.
		link.transition()
			.duration(duration)
			.attr("d", diagonal);

		// Transition exiting nodes to the parent's new position.
		link.exit().transition()
			.duration(duration)
			.attr("d", function (d) {
			var o = {
				x: source.x,
				y: source.y
			};
			return diagonal({
				source: o,
				target: o
			});
		})
			.remove();

		// Stash the old positions for transition.
		nodes.forEach(function (d) {
			d.x0 = d.x;
			d.y0 = d.y;
		});
		var circle = node.selectAll("circle")
		
		// Control-click to expand row, animate click
		circle.on('click', function (d) {
		  function toggleRow(d) {
				if (d._children) {
					d._children.forEach(toggleRow);
					toggle(d);
				}
			  }
		
		    if(window.event.ctrlKey){
			  if (d._children){
			    d._children.forEach(toggleRow);
			  }
			}
			d3.select(this).attr("r", 12);
		});
	}

	// Toggle children.
	function toggle(d) {
		if (d.children) {
			d._children = d.children;
			d.children = null;
		} else {
			d.children = d._children;
			d._children = null;
		}
	}

	function mouseover(d) {
		d3.select(this).append("text")
			.attr("class", "hover")
			.attr('transform', function (d) {
			return 'translate(5, -10)';
		})
			.text(d.name + ": " + d.id);
	}

	// Toggle children on click.
	function mouseout(d) {
		d3.select(this).select("text.hover").remove();
	}
	
});