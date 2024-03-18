// script.js
const paragraphs = document.querySelectorAll('p');

// paragraphs.forEach(paragraph => {
//   paragraph.addEventListener('mouseover', () => {
//     paragraph.classList.add('highlight');
//     const timestamp = paragraph.getAttribute('data-timestamp');
//     console.log(`Associated timestamp: ${timestamp}`);
//   });

//   paragraph.addEventListener('mouseout', () => {
//     paragraph.classList.remove('highlight');
//   });
// });

// Add event listeners to paragraphs
paragraphs.forEach(paragraph => {
  paragraph.addEventListener('mouseover', event => {
      paragraph.classList.add('highlight');
      const startTime = paragraph.getAttribute('data-timestamp-start');
      const endTime = paragraph.getAttribute('data-timestamp-end');
      const bubble = createTimestampBubble(startTime, endTime);
      document.body.appendChild(bubble);

      // Position the bubble next to the cursor
      updateBubblePosition(event, bubble);

      // Update the bubble position as the cursor moves
      document.addEventListener('mousemove', event => {
          updateBubblePosition(event, bubble);
      });
  });

  paragraph.addEventListener('mouseout', () => {
      paragraph.classList.remove('highlight');
      const bubble = document.querySelector('.timestamp-bubble');
      if (bubble) {
          bubble.remove();
      }
  });
});

function createTimestampBubble(startTime, endTime) {
  const bubble = document.createElement('div');
  bubble.classList.add('timestamp-bubble');
  bubble.textContent = `start: ${startTime}, end: ${endTime}`;
  return bubble;
}

function updateBubblePosition(event, bubble) {
  const offsetX = 10;
  const offsetY = -30; // Adjust the offset to position the bubble above the cursor
  bubble.style.left = event.pageX + offsetX + 'px';
  bubble.style.top = event.pageY + offsetY + 'px';
}



