
class ButtonStyles(object):
  grey_button = """
          -moz-box-shadow:inset 0px 1px 0px 0px #ffffff;
          -webkit-box-shadow:inset 0px 1px 0px 0px #ffffff;
          box-shadow:inset 0px 1px 0px 0px #ffffff;
          background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #ededed), color-stop(1, #dfdfdf));
          background:-moz-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
          background:-webkit-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
          background:-o-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
          background:-ms-linear-gradient(top, #ededed 5%, #dfdfdf 100%);
          background:linear-gradient(to bottom, #ededed 5%, #dfdfdf 100%);
          filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#ededed', endColorstr='#dfdfdf',GradientType=0);
          background-color:#ededed;
          border:1px solid #dcdcdc;
          display:inline-block;
          cursor:pointer;
          color:#777777;
          font-family:Arial;
          font-size:15px;
          font-weight:bold;
          padding:6px 24px;
          text-decoration:none;
          text-shadow:0px 1px 0px #ffffff;
      """

  turquoise_shadowed = """
      -moz-box-shadow: 0px 10px 14px -7px #276873;
      -webkit-box-shadow: 0px 10px 14px -7px #276873;
      box-shadow: 0px 10px 14px -7px #276873;
      background:-webkit-gradient(linear, left top, left bottom, color-stop(0.05, #599bb3), color-stop(1, #408c99));
      background:-moz-linear-gradient(top, #599bb3 5%, #408c99 100%);
      background:-webkit-linear-gradient(top, #599bb3 5%, #408c99 100%);
      background:-o-linear-gradient(top, #599bb3 5%, #408c99 100%);
      background:-ms-linear-gradient(top, #599bb3 5%, #408c99 100%);
      background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);
      filter:progid:DXImageTransform.Microsoft.gradient(startColorstr='#599bb3', endColorstr='#408c99',GradientType=0);
      background-color:#599bb3;
      -moz-border-radius:8px;
      -webkit-border-radius:8px;
      border-radius:8px;
      display:inline-block;
      cursor:pointer;
      color:#ffffff;
      font-family:Arial;
      font-size:20px;
      font-weight:bold;
      padding:13px 32px;
      text-decoration:none;
      text-shadow:0px 1px 0px #3d768a;
  """

  push_button = """
    display: inline-block;
    border: none;
    border-radius: .3em;
    box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.1), inset 0 -0.25em 0 rgba(0, 0, 0, 0.25), 0 0.25em 0.25em rgba(0, 0, 0, 0.05);
    color: #fff;
    cursor: pointer;
    font-family: 'Raleway', sans-serif;
    font-weight: 300;
    line-height: 1.5;
    letter-spacing: 1px;
    padding: .5em 1.5em .75em;
    position: relative;
    text-decoration: none;
    text-shadow: 0 1px 1px rgba(255, 255, 255, 0.25);
    vertical-align: middle;
    -webkit-user-select: none;
       -moz-user-select: none;
        -ms-user-select: none;
            user-select: none;
  """