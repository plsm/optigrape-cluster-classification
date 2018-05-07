library ("data.table")
library ("ggplot2")

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


## Create an image plot with the median success rate of classifiers.  The data
## set was composed of two classes.
##
## The experiment filename is a CSV file with columns: filename with classifiers
## parameters and success rate, names of class A and B, learning parameters, and
## fraction test.
##
create.success.rate.image.plot.for.2.classes <- function (
  experiment.filename
) {
  experiments <- fread (experiment.filename)
  data <- experiments [
    ,
    fread (filename),
    by = .(
      filename,
      class.A,
      class.B,
      learning.parameters,
      fraction.test
    )
  ]
  data.to.plot <- data [
    ,
    .(
      value = median (score)
    ),
    keyby = .(
      class.A,
      class.B,
      learning.parameters,
      fraction.test
    )
  ]
  plot.performance <- function (
    subset.data,
    learning.parameters,
    fraction.test
  ) {
    graphics <- ggplot (
      data = subset.data
    ) + geom_point (
      mapping = aes (
        x = class.A,
        y = class.B,
        color = value,
        size = value
      )
    ) + scale_colour_gradient (
      low = "#FF0000",
      high = "#00FF00",
      labels = function (v) return (sprintf ("%d%%", v * 100))
    ) + scale_size (
      labels = function (v) return (sprintf ("%d%%", v * 100))
    ) + theme_bw (
    ) + labs (
      title = "median of classifier success rate in a data set with two classes",
      x = "class A",
      y = "class B",
      colour = "success rate",
      size = "success rate"
    )
    ggsave (
      filename = sprintf (
        "success-rate_2-class-data-set_%s_%.2f.png",
        learning.parameters,
        fraction.test
      ),
      device = "png",
      scale = 1,
      plot = graphics,
      width = 2.1 + nrow (subset.data [, 1, by = .(class.A)]) * 5.7 / 7,
      height = 4,
      units = "in"
    )
    return (0)
  }
  data.to.plot [
    ,
    plot.performance (
      .SD,
      learning.parameters,
      fraction.test
    ),
    by = .(
      learning.parameters,
      fraction.test
    )
  ]
}
