document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById('drop-zone');
  const codeBlocks = document.querySelectorAll('.code-block');

  codeBlocks.forEach(block => {
    block.addEventListener('dragstart', (e) => {
      e.dataTransfer.setData('text/plain', e.target.id);
      e.target.style.opacity = '0.5';
    });

    block.addEventListener('dragend', (e) => {
      e.target.style.opacity = '1';
    });
  });

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('hover');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('hover');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('hover');
    const droppedElementId = e.dataTransfer.getData('text/plain');
    const droppedElement = document.getElementById(droppedElementId);

    dropZone.textContent = droppedElement.textContent;

    if (droppedElementId === 'option-correct') {
      dropZone.classList.remove('incorrect');
      dropZone.classList.add('correct');
    } else {
      dropZone.classList.remove('correct');
      dropZone.classList.add('incorrect');
    }
  });
});