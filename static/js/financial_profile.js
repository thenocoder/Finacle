document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("profileForm");

    if (!form) {
        return;
    }

    const steps = Array.from(
        form.querySelectorAll(".step")
    );

    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");
    const submitBtn = document.getElementById("submitBtn");
    const progressBar = document.getElementById("progressBar");

    if (
        !steps.length ||
        !nextBtn ||
        !prevBtn ||
        !submitBtn
    ) {
        return;
    }


    /* =========================================================
       STATE
    ========================================================= */

    let currentStep = 0;


    /* =========================================================
       SHOW STEP
    ========================================================= */

    function showStep(index) {

        if (index < 0) {
            index = 0;
        }

        if (index >= steps.length) {
            index = steps.length - 1;
        }

        currentStep = index;


        /* Hide all steps */

        steps.forEach(function (step, i) {

            if (i === currentStep) {

                step.classList.remove("d-none");
                step.classList.add("active");

            } else {

                step.classList.add("d-none");
                step.classList.remove("active");

            }

        });


        /* Previous button */

        if (currentStep === 0) {

            prevBtn.classList.add("d-none");

        } else {

            prevBtn.classList.remove("d-none");

        }


        /* Next / Submit buttons */

        if (currentStep === steps.length - 1) {

            nextBtn.classList.add("d-none");
            submitBtn.classList.remove("d-none");

        } else {

            nextBtn.classList.remove("d-none");
            submitBtn.classList.add("d-none");

        }


        /* Progress */

        if (progressBar) {

            const progress =
                ((currentStep + 1) / steps.length) * 100;

            progressBar.style.width = progress + "%";

        }

    }


    /* =========================================================
       VALIDATE CURRENT STEP
    ========================================================= */

    function validateCurrentStep() {

        const current =
            steps[currentStep];

        if (!current) {
            return true;
        }


        /*
         * Only validate controls that are
         * actually inside the current step.
         */

        const requiredFields =
            current.querySelectorAll("[required]");


        for (const field of requiredFields) {

            if (!field.checkValidity()) {

                field.reportValidity();

                return false;
            }

        }

        return true;
    }


    /* =========================================================
       NEXT
    ========================================================= */

    nextBtn.addEventListener("click", function () {

        if (!validateCurrentStep()) {
            return;
        }

        if (currentStep < steps.length - 1) {

            showStep(currentStep + 1);

        }

    });


    /* =========================================================
       PREVIOUS
    ========================================================= */

    prevBtn.addEventListener("click", function () {

        if (currentStep > 0) {

            showStep(currentStep - 1);

        }

    });


    /* =========================================================
       SAVE PROFILE
       
       IMPORTANT:
       Do NOT prevent the form submission.
       Flask must receive the POST request.
    ========================================================= */

    form.addEventListener("submit", function (event) {

        /*
         * Validate the final step only.
         */

        if (!validateCurrentStep()) {

            event.preventDefault();

            return;

        }

        /*
         * DO NOT call:
         *
         * event.preventDefault()
         *
         * here.
         *
         * The browser must submit the form to:
         *
         * /financial-profile/
         */

        submitBtn.disabled = true;

        submitBtn.innerHTML =
            "Saving Profile...";

    });


    /* =========================================================
       INITIAL STATE
    ========================================================= */

    showStep(0);

});
