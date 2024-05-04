// JavaScript
function viewImage(imageUrl, imageName) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImage");
    modal.style.display = "block";
    modalImg.src = imageUrl;
    modalImg.alt = imageName;
}

function closeModal() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}

