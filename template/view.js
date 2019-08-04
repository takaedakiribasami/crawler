run(data);

function run(data) {
    let width = document.documentElement.clientWidth;
    let height = document.documentElement.clientHeight;

    let root = initRoot(height / 2, width / 2, data);
    let node_cnt = 0;

    d3.select("body")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    d3.select("svg")
        .append("g")
        .attr("class", "all")
        .attr("transform", "translate(80,0)");

    let zoom = d3.zoom()
        .scaleExtent([0.01, 10])
        .on("zoom", zoomed);
    d3.select("svg").call(zoom);

    d3.tree(root).size([height, width]);
    setNodeId(root);
    closeAll(root);
    update(root, root, node_cnt);
}


function initRoot(x, y, data) {
    let root = d3.hierarchy(data);
    root.x0 = x;
    root.y0 = y;
    root.x = x;
    root.y = y;
    return root;
}

function zoomed() {
    d3.select(".all").attr("transform", d3.event.transform);
}

// node action on click
function toggle(node) {
    if (node.children) {
        node._children = node.children;
        node.children = null;
    } else {
        node.children = node._children;
        node._children = null;
    }
}

function closeAll(node) {
    if (!node.children)
        return
    toggle(node);
    for (let i = 0; i < node._children.length; i++) {
        closeAll(node._children[i]);
    }
}


// get width of each level
function childCount(node, level, levelWidth) {
    if (node.children && node.children.length > 0) {
        if (levelWidth.length <= level + 1)
            levelWidth.push(0);
        levelWidth[level + 1] += node.children.length;
        for (let i = 0; i < node.children.length; i++) {
            levelWidth = childCount(node.children[i], level + 1, levelWidth);
        }
    }
    return levelWidth;
}

function setNodeId(root) {
    nodes = root.descendants();
    for (let i = 0; i < nodes.length; i++) {
        nodes[i].nid = i;
    }
}

function setXY(node) {
    let parent_x = node.x;
    let parent_y = node.y;
    let level = node.depth + 1;
    let offset = 0;
    if (!node.children) return 0;
    for (let i = 0; i < node.children.length; i++) {
        node.children[i].x0 = parent_x;
        node.children[i].y0 = parent_y;
        node.children[i].x = i * 70 + parent_x + offset;
        node.children[i].y = level * 500 + parent_y;
        offset += setXY(node.children[i]);
    }
    return node.children.length * 70;
}

function setNewSize(root) {
    let levelWidth = [1];
    levelWidth = childCount(root, 0, levelWidth);

    newHeight = d3.max(levelWidth) * 25;
    newWidth = levelWidth.length * 400;
    d3.tree(root).size([newHeight, newWidth]);
}

function setDetail(node) {
    let div = d3.select("#detail");
    div.transition().duration(200)
    let pid = node.parent ? node.parent.nid : null;
    let pname = node.parent ? node.parent.data.name : null;
    div.html("<p>CURRENT (" + node.nid + ") : " + node.data.name + "</p>"
        + "<p>PARENT (" + pid + ") : " + pname + "</p > ");
}


function update(root, source, node_cnt) {
    setNewSize(root);
    setXY(root);

    let node = d3.select('.all').selectAll('.node')
        .data(root.descendants(),
            function (d) { return d.id || (d.id = ++node_cnt); });

    let nodeEnter = node.enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", "translate(" + source.y + "," + source.x + ")")
        .on("click", function (d) {
            toggle(d);
            update(root, d, node_cnt);
        })
        .on("mouseover", setDetail);

    nodeEnter.append("circle")
        .attr("r", 12)
        .style("fill", function (d) {
            return d._children ? "gray" : "#fff";
        });

    nodeEnter.append("text")
        .attr("y", -15)
        .attr("dy", "3")
        .attr("font-size", "250%")
        .attr("text-anchor", "middle")
        .text(function (d) {
            return d.nid;
        })
        .style("fill-opacity", 1e-6);

    let duration = 500;
    let nodeUpdate = nodeEnter.merge(node);
    nodeUpdate.transition()
        .duration(duration)
        .attr("transform", function (d) {
            return "translate(" + d.y + "," + d.x + ")";
        });

    nodeUpdate.select("circle")
        .attr("r", 8)
        .style("fill", function (d) {
            return d._children ? "gray" : "#fff";
        });

    nodeUpdate.select("text").style("fill-opacity", 1);


    let nodeExit = node.exit()
        .transition()
        .duration(duration)
        .attr("transform", "translate(" + source.y + "," + source.x + ")")
        .remove();

    nodeExit.select("circle").attr("r", 0);

    nodeExit.select("text").style("fill-opacity", 1e-6);


    let link = d3.select(".all").selectAll(".link")
        .data(root.links(), function (d) {
            return d.target.id;
        });

    let linkEnter = link.enter()
        .insert('path', "g")
        .attr("class", "link")
        .attr("d", d3.linkHorizontal()
            .x(source.y)
            .y(source.x)
        );

    var linkUpdate = linkEnter.merge(link);
    linkUpdate.transition()
        .duration(duration)
        .attr("d", d3.linkHorizontal()
            .x(function (d) { return d.y; })
            .y(function (d) { return d.x; })
        );

    link.exit()
        .transition()
        .duration(duration)
        .attr("d", d3.linkHorizontal()
            .x(function (d) { return source.y; })
            .y(function (d) { return source.x; })
        )
        .remove();
}
