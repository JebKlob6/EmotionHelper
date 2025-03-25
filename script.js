

document.addEventListener('DOMContentLoaded', function() {
    // Global array to track selected symptoms
    let selectedSymptoms = [];

    // Emotion data structure
    const emotionData = [
        // HAPPY
        ["Happy", "Content", "Playful"],
        ["Happy", "Content", "Free"],
        ["Happy", "Content", "Joyful"],
        ["Happy", "Interested", "Curious"],
        ["Happy", "Interested", "Inquisitive"],
        ["Happy", "Proud", "Successful"],
        ["Happy", "Proud", "Confident"],
        ["Happy", "Accepted", "Respected"],
        ["Happy", "Accepted", "Valued"],
        ["Happy", "Powerful", "Courageous"],
        ["Happy", "Powerful", "Creative"],
        ["Happy", "Peaceful", "Loving"],
        ["Happy", "Peaceful", "Thankful"],
        ["Happy", "Trusting", "Sensitive"],
        ["Happy", "Trusting", "Intimate"],
        
        // SURPRISED
        ["Surprised", "Excited", "Energetic"],
        ["Surprised", "Excited", "Eager"],
        ["Surprised", "Amazed", "Awe"],
        ["Surprised", "Amazed", "Astonished"],
        ["Surprised", "Confused", "Perplexed"],
        ["Surprised", "Confused", "Disillusioned"],
        ["Surprised", "Startled", "Shocked"],
        ["Surprised", "Startled", "Dismayed"],
        ["Surprised", "Unfocused", "Distracted"],
        ["Surprised", "Unfocused", "Sleepy"],
        
        // BAD
        ["Bad", "Stressed", "Out of control"],
        ["Bad", "Stressed", "Overwhelmed"],
        ["Bad", "Busy", "Pressured"],
        ["Bad", "Busy", "Rushed"],
        ["Bad", "Bored", "Apathetic"],
        ["Bad", "Bored", "Indifferent"],
        ["Bad", "Tired", "Unfocused"],
        ["Bad", "Tired", "Sleepy"],
        ["Bad", "Anxious", "Overwhelmed"],
        ["Bad", "Anxious", "Scared"],
        
        // FEARFUL
        ["Fearful", "Scared", "Helpless"],
        ["Fearful", "Scared", "Frightened"],
        ["Fearful", "Anxious", "Worried"],
        ["Fearful", "Anxious", "Overwhelmed"],
        ["Fearful", "Insecure", "Inferior"],
        ["Fearful", "Insecure", "Inadequate"],
        ["Fearful", "Weak", "Worthless"],
        ["Fearful", "Weak", "Insignificant"],
        ["Fearful", "Rejected", "Excluded"],
        ["Fearful", "Rejected", "Persecuted"],
        ["Fearful", "Threatened", "Nervous"],
        ["Fearful", "Threatened", "Exposed"],
        
        // ANGRY
        ["Angry", "Distant", "Withdrawn"],
        ["Angry", "Distant", "Numb"],
        ["Angry", "Critical", "Skeptical"],
        ["Angry", "Critical", "Dismissive"],
        ["Angry", "Disgusted", "Disapproving"],
        ["Angry", "Disgusted", "Judgmental"],
        ["Angry", "Disapproving", "Embarrassed"],
        ["Angry", "Disapproving", "Disappointed"],
        ["Angry", "Awful", "Nauseated"],
        ["Angry", "Awful", "Detestable"],
        ["Angry", "Repelled", "Horrified"],
        ["Angry", "Repelled", "Hesitant"],
        ["Angry", "Aggressive", "Hostile"],
        ["Angry", "Aggressive", "Provoked"],
        ["Angry", "Mad", "Jealous"],
        ["Angry", "Mad", "Furious"],
        ["Angry", "Bitter", "Indignant"],
        ["Angry", "Bitter", "Violated"],
        ["Angry", "Humiliated", "Ridiculed"],
        ["Angry", "Humiliated", "Disrespected"],
        ["Angry", "Let down", "Betrayed"],
        ["Angry", "Let down", "Resentful"],
        
        // SAD
        ["Sad", "Lonely", "Isolated"],
        ["Sad", "Lonely", "Abandoned"],
        ["Sad", "Vulnerable", "Victimized"],
        ["Sad", "Vulnerable", "Fragile"],
        ["Sad", "Despair", "Grief"],
        ["Sad", "Despair", "Powerless"],
        ["Sad", "Guilty", "Ashamed"],
        ["Sad", "Guilty", "Remorseful"],
        ["Sad", "Depressed", "Empty"],
        ["Sad", "Depressed", "Inferior"],
        ["Sad", "Hurt", "Disappointed"],
        ["Sad", "Hurt", "Embarrassed"]
    ];

    // Color mapping for each primary emotion
    const colorMap = {
        'Happy': 'rgba(224, 122, 95, 1)',     // Slightly darker, 70% opacity
        'Surprised': 'rgba(242, 204, 143, 1)', // Slightly darker, 70% opacity
        'Bad': 'rgba(129, 178, 154, 1)',       // Slightly darker, 70% opacity
        'Fearful': 'rgba(61, 133, 198, 1)',    // Slightly darker, 70% opacity
        'Angry': 'rgba(149, 117, 205, 1)',     // Slightly darker, 70% opacity
        'Sad': 'rgba(229, 115, 115, 1)'        // Slightly darker, 70% opacity
    };

  // Format the data for D3's hierarchy
  function formatData(data) {
    const root = { name: "root", children: [] };
    const primaryMap = {};
    data.forEach(entry => {
      const [primary, secondary, tertiary] = entry;
      if (!primaryMap[primary]) {
        const primaryNode = { name: primary, children: [] };
        primaryMap[primary] = primaryNode;
        root.children.push(primaryNode);
      }
      const primaryNode = primaryMap[primary];
      let secondaryNode = primaryNode.children.find(child => child.name === secondary);
      if (!secondaryNode) {
        secondaryNode = { name: secondary, children: [] };
        primaryNode.children.push(secondaryNode);
      }
      secondaryNode.children.push({ name: tertiary });
    });
    return root;
  }

  // Create tooltip
  const tooltip = d3.select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

  // Format the data
  const root = d3.hierarchy(formatData(emotionData))
    .sum(d => d.children ? 0 : 1);

  // Set up dimensions
  const width = 800;
  const height = 800;
  const radius = Math.min(width, height) / 2;

  // Create the SVG container and save the group element as "g"
  const g = d3.select("#emotion-wheel")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", `translate(${width/2}, ${height/2})`);

  // Create the sunburst partition layout
  const partition = d3.partition()
    .size([2 * Math.PI, radius]);

  // Compute the partition layout
  partition(root);

  // Create an arc generator
  const arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .innerRadius(d => d.y0)
    .outerRadius(d => d.y1);

  // Add the arcs with proper pointer-events so the entire area is clickable
  const path = g.selectAll("path")
    .data(root.descendants().filter(d => d.depth))
    .enter()
    .append("path")
    .attr("d", arc)
    .style("fill", d => {
      if (d.depth === 1) {
        return colorMap[d.data.name];
      } else if (d.depth === 2) {
        return d3.color(colorMap[d.parent.data.name]).brighter(0.5);
      } else {
        return d3.color(colorMap[d.parent.parent.data.name]).brighter(1);
      }
    })
    .style("stroke", "#1a1a2e")
    .style("stroke-width", 1)
    .style("pointer-events", "all")  // Ensure entire area responds to mouse events
    .on("mouseover", function(event, d) {
      d3.select(this)
        .style("opacity", 1)
        .style("stroke-width", 5);
      tooltip.transition()
        .duration(200)
        .style("opacity", 0.9);
      let tooltipText = d.data.name;
      if (d.depth === 3) {
        tooltipText = `${d.parent.parent.data.name} → ${d.parent.data.name} → ${d.data.name}`;
      } else if (d.depth === 2) {
        tooltipText = `${d.parent.data.name} → ${d.data.name}`;
      }
      tooltip.html(tooltipText)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseout", function() {
      d3.select(this)
        .style("opacity", 1)
        .style("stroke-width", 1);
      tooltip.transition()
        .duration(500)
        .style("opacity", 0);
    })
    .on("click", function(event, d) {
      const currentElement = d3.select(this);
      if (currentElement.classed("selected")) {
        currentElement.classed("selected", false);
        selectedSymptoms = selectedSymptoms.filter(item => item !== d.data.name);
      } else {
        currentElement.classed("selected", true);
        selectedSymptoms.push(d.data.name);
      }
      event.stopPropagation();
    });

  // Add the labels and center them in the arcs
  g.selectAll("text")
    .data(root.descendants().filter(d => d.depth && (d.y1 - d.y0) > 10))
    .enter()
    .append("text")
    .attr("class", d => `emotion-label ${d.depth === 1 ? 'primary-label' : ''}`)
    .attr("transform", function(d) {
      const x = (d.x0 + d.x1) / 2;
      const y = (d.y0 + d.y1) / 2;
      const rotationDegrees = (x * 180 / Math.PI - 90);
      const translateX = y * Math.cos(x - Math.PI / 2);
      const translateY = y * Math.sin(x - Math.PI / 2);
      return `translate(${translateX},${translateY}) rotate(${rotationDegrees})`;
    })
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .text(d => d.data.name)  // Always show the text (or add your condition)
    .style("fill", "#234",)
    .style("font-weight", "bold");

  // Handle the "Show Selected Symptoms" button click to list highlighted symptoms
  document.getElementById("showSymptomsButton").addEventListener("click", function() {
    const listContainer = document.getElementById("selectedSymptomsList");
    listContainer.innerHTML = "";
    selectedSymptoms.forEach(symptom => {
      const li = document.createElement("li");
      li.textContent = symptom;
      listContainer.appendChild(li);
    });
  });

  // Add a "Spin the Wheel" feature
  document.getElementById("spinButton").addEventListener("click", function() {
    const randomAngle = Math.floor(Math.random() * 360);
    // Animate the rotation of the group element
    g.transition()
      .duration(2000)
      .attrTween("transform", function() {
        // Capture the current rotation by parsing the current transform
        const currentTransform = g.attr("transform");
        // We assume the transform is of the form "translate(width/2, height/2) rotate(angle)"
        const rotateMatch = currentTransform.match(/rotate\(([-\d\.]+)\)/);
        const currentAngle = rotateMatch ? +rotateMatch[1] : 0;
        const interpolate = d3.interpolate(currentAngle, randomAngle);
        return function(t) {
          return `translate(${width/2}, ${height/2}) rotate(${interpolate(t)})`;
        }
      });
  });

  // Optionally, expose the spin functionality globally for debugging
  window.spinWheel = function() {
    document.getElementById("spinButton").click();
  };
});