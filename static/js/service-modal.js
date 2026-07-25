document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById(
        "service-details-modal"
    );
    const modalContent = document.getElementById(
        "service-modal-content"
    );
    const closeButton = document.querySelector(
        ".details-modal-close"
    );
    const serviceLinks = document.querySelectorAll(
        ".service-details-link"
    );

    if (
        !modal ||
        !modalContent ||
        !closeButton ||
        serviceLinks.length === 0
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

    serviceLinks.forEach((link) => {
        link.addEventListener("click", (event) => {
            const templateId = link.dataset.serviceTemplate;
            const template = document.getElementById(templateId);

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

    closeButton.addEventListener("click", closeModal);

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