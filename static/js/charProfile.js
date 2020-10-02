$(document).ready(function () {
  // Calculate the proficiency bonus based on level.
  let profBonus = parseInt($("#level").text());
  console.log(Math.ceil(profBonus / 4));
  $("#prof").text("Proficiency bonus: " + Math.ceil(profBonus / 4));
  // Calculate modifiers based on other attributes and add contextual clues for the user.
  $(".base").each(function () {
    let idString = $(this).attr("id");
    let realStat = $(this).text();
    let modStat = Math.floor((parseInt(realStat) - 10) / 2);

    if ((modStat) => 0) {
      $("#" + idString + "-mod").text("+" + modStat);
    } else if (modStat <= 0) {
      $("#" + idString + "-mod").text("-" + modStat);
    }
  });
  // Mark which saving-throws add the proficiency bonus.
  $(".saving-throw").each(function () {
    if ($(this).hasClass("True") == true) {
      $(this).html('<i class="fas fa-check"></i>');
    } else {
      return;
    }
  });
});
