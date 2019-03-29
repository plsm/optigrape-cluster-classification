library ("data.table")
library ("ggplot2")

## Create a box plot with the success rate of classifiers per different
## parameters.  These parameters can be the data set used, the learning
## algorithm parameters, the relation between the size of learning set and the
## test set, among others.
##
## You should prepare a CSV file with two columns: one with the filename
## containing the data produced by the python module in package
## optigrape_cluster_classification.classifier; the second column should contain
## a description of the parameters used to run the classifier.

create.success.rate.boxplots.2 <- function (
  experiment.filename,
  single.random.chance.win = FALSE,
  condition = NA,
  classifier.success.rate = NA
) {
  # read data ####
  experiments <- fread (experiment.filename)
  data <- experiments [
    ,
    fread (filename),
    by = .(
      filename,
      labels
    )
  ]
  # setup plot ####
  plot <- ggplot (
  ) + geom_boxplot (
    mapping = aes (
      x = labels,
      y = all.score
    ),
    data = data
  ) + scale_y_continuous (
    labels = scales::percent,
    limits = c (0, 1)
  )
  # random classifier success rate ####
  if (single.random.chance.win) {
    ys <- data [, mean (random.chance.win)]
    print (cat (sprintf ("mean random chance to win %f\n", ys)))
    plot <- plot + geom_hline (
      mapping = aes (
        yintercept = ys,
        colour = "red"
      )
    )
  }
  else {
    ys <- data [
      ,
      mean (random.chance.win),
      by = .(
        labels
      )
    ]
    plot <- plot + geom_point (
      mapping = aes (
        x = labels,
        y = V1,
        colour = "red"
      ),
      data = ys,
      shape = 4,
      stroke = 1.5
    ) + scale_colour_manual (
      values = c ("red"),
      labels = c (NULL)
    )
  }
  # plot common stuff ####
  plot <- plot + labs (
    y = ifelse (
      is.na (classifier.success.rate),
      "classifier success rate",
      classifier.success.rate),
    x = ifelse (
      is.na (condition),
      "condition",
      condition),
    colour = "random\nchance\nto win"
  ) +
    theme_bw () +
    coord_flip ()
  # save plot ####
  ggsave (
    filename = "success-rate.png",
    plot = plot
  )
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
      labels = function (v) return (sprintf ("%.0f%%", v * 100))
    ) + scale_size (
      labels = function (v) return (sprintf ("%.0f%%", v * 100))
    ) + theme_bw (
    ) + labs (
      title = "median of classifier success rate\nin a data set with two classes",
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
