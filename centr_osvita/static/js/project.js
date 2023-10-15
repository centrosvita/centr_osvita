/* Project specific Javascript goes here. */
if ($("#time").length) {
  const renderTimer = (min, sec) => {
    if (min < 10) {
      min = "0" + min;
    }
    if (sec < 10) {
      sec = "0" + sec;
    }
    $("#timer").html(`${min}:${sec}`);
  };
  $("#timeoutModal").on("hide.bs.modal", e => {
    window.location.replace($("#timeout-results").attr("href"));
  });

  let time = +$("#time").html();
  let minutes = Math.floor(time / 60);
  let seconds = time - minutes * 60;
  renderTimer(minutes, seconds);

  let timer = setInterval(function() {
    if (seconds > 0) {
      seconds--;
    } else if (seconds == 0 && minutes > 0) {
      seconds = 59;
      minutes--;
    } else {
      clearInterval(timer);
      $("#timeoutModal").modal("toggle");
    }
    renderTimer(minutes, seconds);
  }, 1000);
}

if ($("#id_institution_type").length) {
  let input = $("#id_institution_type");

  const handleInstitutionInput = () => {
    if (input.val() == 0 || input.val() == 3) {
      $("#id_grade").css("display", "none");
      $("#id_grade").prop("disabled", true);
      $("#label_for_institution").text("Навчальний заклад");
      if ($("#institution_container").hasClass("col-md-6")) {
        $("#institution_container").toggleClass("col-md-6 col-md-8");
      }
    } else {
      $("#id_grade").css("display", "block");
      $("#id_grade").prop("disabled", false);
      $("#label_for_institution").text("Навчальний заклад та клас");
      if ($("#institution_container").hasClass("col-md-8")) {
        $("#institution_container").toggleClass("col-md-8 col-md-6");
      }
    }
  };

  handleInstitutionInput();

  input.change(e => {
    handleInstitutionInput();
  });
}

if ($("#personal_data_agree") && $("#reg_submit")) {
  let checkbox = $("#personal_data_agree");

  const switchSubmitButtonStatus = () => {
    if (checkbox.is(":checked")) {
      $("#reg_submit").prop("disabled", false);
    } else {
      $("#reg_submit").prop("disabled", true);
    }
  };
  switchSubmitButtonStatus();
  checkbox.change(e => {
    switchSubmitButtonStatus();
  });
}

const parseHtml = (html) => {
  const regex = /<img.*?src="(.*?)".*?>/g;
  const matches = html.match(regex);
  if (matches) {
    matches.forEach((match) => {
      const regexSrc = /src="(.*?)"/g;
      const regexClass = /class="(.*?)"/g;
      const regxStyle = /style="(.*?)"/g;

      const _src = regexSrc.exec(match);
      const _class = regexClass.exec(match);
      const _style = regxStyle.exec(match);

      const src = _src ? _src[1] : '';
      const className = _class ? _class[1] : 'image';
      const style = _style ? _style[1] : '';

      const newImg = `<div class="article__image-wrapper"><img src="${src}" class="${className}" style="${style}"></div>`;
      html = html.replace(match, newImg);
    });
  }

  //wrap all iframes into div witch class "video"
    const regexIframe = /<iframe.*?src="(.*?)".*?><\/iframe>/g;
    const matchesIframe = html.match(regexIframe);
    if (matchesIframe) {
        matchesIframe.forEach((match) => {
            const regexSrc = /src="(.*?)"/g;
            const _src = regexSrc.exec(match);
            const src = _src ? _src[1] : '';
            const newIframe = `<div class="d-flex justify-content-center"><div class="article__video-wrapper"><div class="article__video"><iframe src="${src}"></iframe></div></div></div>`;
            html = html.replace(match, newIframe);
        });
    }


  return html;
}

//search for #blog-article and parse inner html with function parseHtml and paste back
if ($("#blog-article").length) {
    let article = $("#blog-article");
    let html = article.html();
    article.html(parseHtml(html));
}
