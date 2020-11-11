document.addEventListener("DOMContentLoaded", function () {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          console.log(e)
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active"); ``
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      let id = e.target.dataset.id;
      // console.log(id)
      $.get(e.target.href, function (data) {
        // console.log($('#help--slides_' + id))
        // console.log($(data).find('#help--slides_' + id).html())
        $('#help--slides_' + id).html($(data).find('#help--slides_' + id).html())
      });
      const page = e.target.dataset.page;
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function (e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {

    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.$categories = $("input.categories")
      this.currentStep = 1;
      this.categories = new Array();
      this.address;
      this.city;
      this.postcode;
      this.phone;
      this.date;
      this.time;
      this.more_info;
      this.bags;
      this.fundation;
      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];
      this.init();
    }
    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step

      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    getInputValue(name) {
      let $div = $("form")
      return $div.find('[name="' + name + '"]').val();
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;
      //let address;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");
        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      // after step 1 get all institutions based on selected ategories
      if (this.currentStep === 2) {
        let temp = new Array();
        $("input:checked").each(function () {
          temp.push(this.dataset.cat)
        });
        this.categories = temp;
      }
      if (this.currentStep === 3) {
        $("#step_3").empty();
        let address = "/rest/get_institutions/";
        let params = {};
        params.categories = this.categories;
        $.getJSON(address, $.param(params, true), function (data, status) {
          $.each(data, function (key, val) {
            let $div = $("<div>", { "class": "form-group form-group--checkbox" });
            let $label = $("<label>");
            $div.append($label);
            let $input = $("<input>", { "type": "radio", "name": "organization", "value": val.name });
            $label.append($input);
            $label.append($("<span>", { "class": "checkbox radio" }));
            let $span = $("<span>", { "class": "description" });
            $label.append($span);
            $span.append($("<div>", { "class": "title" }).html(val.name));
            $span.append($("<div>", { "class": "subtitle" }).html(val.description));
            $span.append($(document.createElement("div")));
            $("#step_3").append($div);
          });
        });
      }
      if (this.currentStep === 5) {
        this.address = this.getInputValue('address');
        this.city = this.getInputValue('city');
        this.postcode = this.getInputValue('postcode');
        this.phone = this.getInputValue('phone');
        this.date = this.getInputValue('date');
        this.time = this.getInputValue('time');
        this.more_info = this.getInputValue('more_info');
        this.bags = this.getInputValue('bags');
        this.fundation = $('input[name=organization]:checked', this.$form).val()
        let categories = "";
        $("input.categories:checked").each(function () {
          categories = categories + (this.dataset.name);
        })

        // clear div
        let $div_1 = $("#step_5_you_give").empty()
        //add list and items
        let $ul_1 = $("<ul>")
        $div_1.append($ul_1)

        let $li_1 = $("<li>")
        $ul_1.append($li_1)
        $li_1.append($("<span>", { "class": "icon icon-bag" }))
        $li_1.append($("<span>", { "class": "summary--text" })).html(this.bags + " worki " + categories);

        let $li_2 = $("<li>")
        $ul_1.append($li_2)
        $li_2.append($("<span>", { "class": "icon icon-hand" }))
        $li_2.append($("<span>", { "class": "summary--text" })).html('Dla fundacji "' + this.fundation + '"')

        let $div_2 = $("#step_5_address").empty()
        let $ul_2 = $("<ul>")
        $div_2.append($ul_2)
        $ul_2.append($("<li>").html(this.address))
        $ul_2.append($("<li>").html(this.city))
        $ul_2.append($("<li>").html(this.postcode))
        $ul_2.append($("<li>").html(this.phone))

        let $div_3 = $("#step_5_date_time").empty()
        let $ul_3 = $("<ul>")
        $div_3.append($ul_3)
        $ul_3.append($("<li>").html(this.date))
        $ul_3.append($("<li>").html(this.time))
        $ul_3.append($("<li>").html(this.more_info))
      }

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary
    }

    /**
     * Submit form
     *g, let the event go
     * TODO: validation, send data to server
     */
    validate() {
      if (this.categories.length === 0) {
        // category wasn't selected redirect to step 1
        this.currentStep = 1;
        let $div = $("#step_1_form_error").html("");
        $div.append($("<h3>").html("Muisz wybrać przynajmniej jedą kategorię darów."));
        return false;
      }
      else if (this.bags === "") {
        this.currentStep = 2;
        let $div = $("#step_2_form_error").html("");
        $div.append($("<h3>").html("Muisz podać ilość worków."));
        return false;
      }
      else if (!this.fundation) {
        this.currentStep = 3;
        let $div = $("#step_3_form_error").html("");
        $div.append($("<h3>").html("Muisz wybrać fundację."));
        return false;
      }
      else if (this.address === "" || this.date === "" || this.time === "") {
        this.currentStep = 4;
        let $div = $("#step_4_form_error").html("");
        $div.append($("<h3>").html("Muisz podać adres i czas odbioru paczki."));
        return false;
      }
      else return true;

    }

    submit(e) {
      if (this.validate()) {
        this.currentStep++;
        return;
      }
      else {
        e.preventDefault();
        this.updateForm();
      }

    }
  }

  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});
