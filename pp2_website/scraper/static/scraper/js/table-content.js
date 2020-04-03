// Wszystkie komórki
const cells = document.querySelectorAll('.td');

cells.forEach(cell => {
    if (cell.offsetHeight >= 120) cell.classList.add('td-hide')
})

// Komórki o wysokości 100 lub więcej
const big_cells = document.querySelectorAll('.td-hide')

big_cells.forEach(cell => {
    cell.addEventListener('mouseover', () => {
        cell.classList.remove('td-hide')
    })

    cell.addEventListener('mouseout', () => {
        cell.classList.add('td-hide')
    })
})