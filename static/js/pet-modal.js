document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById(
        "pet-details-modal"
    );
    const modalContent = document.getElementById(
        "pet-modal-content"
    );
    const closeButton = document.querySelector(
        ".pet-modal-close"
    );
    const petLinks = document.querySelectorAll(
        ".pet-details-link"
    );

    if (
        !modal ||
        !modalContent ||
        !closeButton ||
        petLinks.length === 0
    ) {
        return;
    }

    function openModal() {
        modal.hidden = false;
        document.body.classList.add("modal-open");
        closeButton.focus();
    }

    function closeModal() {
        modal.hidden = true;
        document.body.classList.remove("modal-open");
    }

    petLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const templateId = link.dataset.petTemplate;
            const template = document.getElementById(
                templateId
            );

            if (!template) {
                return;
            }

            event.preventDefault();

            modalContent.innerHTML = "";
            modalContent.appendChild(
                template.content.cloneNode(true)
            );

            openModal();
        });
    });

    closeButton.addEventListener(
        "click",
        closeModal
    );

    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });
});