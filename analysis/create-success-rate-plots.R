library ("data.table")

create.success.rate.boxplots <- function (
  experiment.filename
) {
  experiments <- fread (experiment.filename)
  data <- experiments [
    ,
    fread (filename),
    by = .(
      filename,
      data.sets,
      learning.parameters,
      fraction.test
    )
  ]
  plot.performance <- function (
    show.iterations.performed = FALSE
  ) {
    par (
      mar = c (4, 30, 5, 2)
    )
    boxplot (
      formula = score~data.sets+learning.parameters+fraction.test,
      data = data,
      ylim = c (0, 1),
      main = "classification score versus data sets and learning parameters",
      ylab = NA,
      xlab = "score",
      horizontal = TRUE,
      las = 1
    )
    if (show.iterations.performed) {
      Ns <- data [
        ,
        .N,
        by = .(
          data.sets,
          learning.parameters,
          fraction.test
        )]
      axis (
        side = 4,
        at = seq (1, nrow (Ns)),
        labels = Ns [, N],
        las = 1
      )
    }
    abline (
      v = data [, mean (random.chance.win)],
      lty = 3
    )
  }
  png (
    filename = "performance.png",
    width = 1400,
    height = 900
  )
  plot.performance ()
  dev.off ()
}
