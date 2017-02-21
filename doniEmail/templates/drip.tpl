<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="format-detection" content="telephone=no" /> <!-- disable auto telephone linking in iOS -->

  <link href="https://fonts.googleapis.com/css?family=Lato:300,400,700" rel="stylesheet">

  <title>Welcome to Platso</title>
  <style type="text/css">
    /* RESET STYLES */
    #contentContainer{
        box-shadow: 5px 5px 5px rgba(208, 202, 202, 0.68);
    }
    #LinkButton{margin-left: auto;
    margin-right: auto;
    transition: all 0.3s !important;
    color: #fff !important;
    background: rgba(245, 130, 51, 0.85) !important;
    border: 2px solid #F58233 !important;
    border-radius: 4px !important;
    width: 201px;
    text-align: center;
    cursor: pointer;
    padding: 10px 10px 10px 10px;}
    #LinkButtonAnchor{
    color: #fff;
    text-decoration: none !important;
    }
    #LinkAddress{
    	text-align: center;
    font-size: 10px;
    margin-top: -10px;
    font-stretch: semi-condensed;
    }
    html { background-color:#F9F9F9; margin:0; padding:0; }
    body, #bodyTable, #bodyCell, #bodyCell{height:100% !important; margin:0; padding:0; width:100% !important;font-family: 'Lato', sans-serif;}
    table{border-collapse:collapse;}
    table[id=bodyTable] {width:100%!important;margin:auto;max-width:500px!important;color:#7A7A7A;font-weight:normal;}
    img, a img{border:0; outline:none; text-decoration:none;height:40px; line-height:100%;}
    a {text-decoration:none !important;border-bottom: 1px solid;}
    h1, h2, h3, h4, h5, h6{color:#5F5F5F; font-weight:normal; font-family:Helvetica; font-size:20px; line-height:125%; text-align:Left; letter-spacing:normal;margin-top:0;margin-right:0;margin-bottom:10px;margin-left:0;padding-top:0;padding-bottom:0;padding-left:0;padding-right:0;}

    /* CLIENT-SPECIFIC STYLES */
    .ReadMsgBody{width:100%;} .ExternalClass{width:100%;} /* Force Hotmail/Outlook.com to display emails at full width. */
    .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div{line-height:100%;} /* Force Hotmail/Outlook.com to display line heights normally. */
    table, td{mso-table-lspace:0pt; mso-table-rspace:0pt;} /* Remove spacing between tables in Outlook 2007 and up. */
    #outlook a{padding:0;} /* Force Outlook 2007 and up to provide a "view in browser" message. */
    img{-ms-interpolation-mode: bicubic;outline:none; text-decoration:none;} /* Force IE to smoothly render resized images. */
    body, table, td, p, a, li, blockquote{-ms-text-size-adjust:100%; -webkit-text-size-adjust:100%; font-weight:normal!important;} /* Prevent Windows- and Webkit-based mobile platforms from changing declared text sizes. */
    .ExternalClass td[class="ecxflexibleContainerBox"] h3 {padding-top: 10px !important;} /* Force hotmail to push 2-grid sub headers down */

    /* /\/\/\/\/\/\/\/\/ TEMPLATE STYLES /\/\/\/\/\/\/\/\/ */

    /* ========== Page Styles ========== */
    h1{display:block;font-size:26px;font-style:normal;font-weight:normal;line-height:100%;}
    h2{display:block;font-size:20px;font-style:normal;font-weight:normal;line-height:120%;}
    h3{display:block;font-size:17px;font-style:normal;font-weight:normal;line-height:110%;}
    h4{display:block;font-size:18px;font-style:normal;font-weight:normal;line-height:100%;}
    .flexibleImage{height:auto;}
    .linkRemoveBorder{border-bottom:0 !important;}
    .textContent {
      font-style: normal!important;
      font-family: 'Helvitica', Arial, sans-serif!important;
      font-size: 16px!important;
    }
    table[class=flexibleContainerCellDivider] {padding-bottom:0 !important;padding-top:0 !important;}

    body, #bodyTable{background-color:#F0F0F0;}
    #emailHeader{background-color:#F0F0F0;}
    #emailBody{width:80%; background-color:#F0F0F0;}
    #emailFooter{background-color:#F0F0F0;}
    .nestedContainer{background-color:#F8F8F8; border:1px solid #CCCCCC;}
    .emailButton{background-color:#205478; border-collapse:separate;}
    #buttonContent{
    padding: 10px 40px;
    -webkit-transition: all .3s;
    -moz-transition: all .3s;
    transition: all .3s;
    background: rgba(245,130,51,.85);
    border: 2px solid #F58233;
    border-radius: 4px;
    cursor:pointer;
    }


    #buttonContent:hover{background: rgba(245,130,51,1)}
    .buttonContent a{color:#FFFFFF; display:block; text-decoration:none!important; border:0!important;letter-spacing:1px;}
    .emailCalendar{background-color:#FFFFFF; border:1px solid #CCCCCC;}
    .emailCalendarMonth{background-color:#205478; color:#FFFFFF; font-family:Helvetica, Arial, sans-serif; font-size:16px; font-weight:bold; padding-top:10px; padding-bottom:10px; text-align:center;}
    .emailCalendarDay{color:#205478; font-family:Helvetica, Arial, sans-serif; font-size:60px; font-weight:bold; line-height:100%; padding-top:20px; padding-bottom:20px; text-align:center;}
    .imageContentText {margin-top: 10px;line-height:0;}
    .imageContentText a {line-height:0;}
    #invisibleIntroduction {display:none !important;} /* Removing the introduction text from the view */

    /*FRAMEWORK HACKS & OVERRIDES */
    span[class=ios-color-hack] a {color:#275100!important;text-decoration:none!important;} /* Remove all link colors in IOS (below are duplicates based on the color preference) */
    span[class=ios-color-hack2] a {color:#205478!important;text-decoration:none!important;}
    span[class=ios-color-hack3] a {color:#8B8B8B!important;text-decoration:none!important;}

    .a[href^="tel"], a[href^="sms"] {text-decoration:none!important;color:#606060!important;pointer-events:none!important;cursor:default!important;}
    .mobile_link a[href^="tel"], .mobile_link a[href^="sms"] {text-decoration:none!important;color:#606060!important;pointer-events:auto!important;cursor:default!important;}

    /* MOBILE STYLES */
    @media only screen and (max-width: 480px){
      /*////// CLIENT-SPECIFIC STYLES //////*/
      body{width:100% !important; min-width:100% !important;} /* Force iOS Mail to render the email at full width. */

      table[id="emailHeader"],
      table[id="emailBody"],
      table[id="emailFooter"],
      table[class="flexibleContainer"],
      td[class="flexibleContainerCell"] {width:100% !important;}
      td[class="flexibleContainerBox"], td[class="flexibleContainerBox"] table {display: block;width: 100%;text-align: left;}

      td[class="imageContent"] img {height:40px !important; width:40px !important; max-width:100% !important; }
      img[class="flexibleImage"]{height:40px !important; width:40px !important;max-width:100% !important;}
      img[class="flexibleImageSmall"]{height:40px !important; width:40px !important;}

      table[class="flexibleContainerBoxNext"]{padding-top: 10px !important;}
      table[class="emailButton"]{width:100% !important;}
      td[class="buttonContent"]{padding:0 !important;}
      td[class="buttonContent"] a{padding:15px !important;}

    }

    /*  CONDITIONS FOR ANDROID DEVICES ONLY
    *   http://developer.android.com/guide/webapps/targeting.html
    *   http://pugetworks.com/2011/04/css-media-queries-for-targeting-different-mobile-devices/ ;
    =====================================================*/

    @media only screen and (-webkit-device-pixel-ratio:.75){
      /* Put CSS for low density (ldpi) Android layouts in here */
    }

    @media only screen and (-webkit-device-pixel-ratio:1){
      /* Put CSS for medium density (mdpi) Android layouts in here */
    }

    @media only screen and (-webkit-device-pixel-ratio:1.5){
      /* Put CSS for high density (hdpi) Android layouts in here */
    }
    /* end Android targeting */

    /* CONDITIONS FOR IOS DEVICES ONLY
    =====================================================*/
    @media only screen and (min-device-width : 320px) and (max-device-width:568px) {

    }
    /* end IOS targeting */
  </style>
  <!--
    Outlook Conditional CSS

    These two style blocks target Outlook 2007 & 2010 specifically, forcing
    columns into a single vertical stack as on mobile clients. This is
    primarily done to avoid the 'page break bug' and is optional.

    More information here:
    http://templates.mailchimp.com/development/css/outlook-conditional-css
  -->
  <!--[if mso 12]>
    <style type="text/css">
      .flexibleContainer{display:block !important; width:100% !important;}
    </style>
  <![endif]-->
  <!--[if mso 14]>
    <style type="text/css">
      .flexibleContainer{display:block !important; width:100% !important;}
    </style>
  <![endif]-->
</head>
<body style="background: #F0F0F0" leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
  <center style="">
    <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="table-layout: fixed;max-width:100% !important;width: 100% !important;min-width: 100% !important;">
      <tr>
        <td align="center" valign="top" id="bodyCell">

          <table border="0" cellpadding="0" cellspacing="0" width="500" id="emailBody">



            <tr >
              <td align="center" valign="top">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tr>
                    <td align="center" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" width="500" class="flexibleContainer">
                        <tr>
                          <td align="center" valign="top" width="500" class="flexibleContainerCell">
                            <table border="0" cellpadding="30" cellspacing="0" width="100%">
                              <tr>
                                <td style="padding: 15px 30px;background: #F0F0F0;" align="center" valign="top">
                                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                      <td valign="middle" class="textContent" style="text-align: center;">
                                        <div style="margin-top: 25px; margin-bottom: 15px;">
                                          <img height="45" width="170" style="vertical-align: middle; height:45px;display:inline-block; padding: 8px;" src="cid:logo-dark.png">
                                        </div>
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <tr>
              <td align="center" valign="top">
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tr>
                    <td align="center" valign="top">
                      <table border="0" cellpadding="0" cellspacing="0" width="100%" class="flexibleContainer">
                        <tr>
                          <td align="center" valign="top" width="100%" class="flexibleContainerCell">
                            <table border="0" cellpadding="" cellspacing="0" width="100%">
                              <tr>
                                <td style="" align="center" valign="top">
                                  <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                      <td valign="top" class="textContent">
                                        <div id="contentContainer" style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:13px!important;color:black;line-height:135%; background: #FFFFFF;
    										margin-bottom: 10px;">

                                          <div style="height:4px;">
                                            <div class="" style="display: inline-block; height:4px; float: left; width: 33.33333333%; background:#DA7B37;"></div>
                                            <div class="" style="display: inline-block; height:4px; float: left; width: 33.33333333%; background:#3DBFF9;"></div>
                                            <div class="" style="display: inline-block; height:4px; float: left; width: 33.33333333%; background:#B08DE5;"></div>
                                          </div>
                                          <div id="content-middle" style="padding:50px 50px 50px 50px;">
                                          	<div style="text-align:left; font-family:Helvetica,Arial,sans-serif;">
												%middle_text
                                          	</div>
                                          </div>
                                          <div style="height:4px;">
                                            <div class="" style="display: inline-block; height:4px; float: left; width: 33.33333333%; background:#DA7B37;"></div>
                                            <div class="" style="display: inline-block; height:4px; float: left; width: 33.33333333%; background:#3DBFF9;"></div>
                                            <div class="" style="display: inline-block; height:4px; float: left; width: 33.33333333%; background:#B08DE5;"></div>
                                          </div>

                                        </div>
                                      </td>
                                    </tr>
                                  </table>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>


          </table>
        </td>
      </tr>
    </table>






    <table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="table-layout: fixed;max-width:100% !important;width: 100% !important;min-width: 100% !important; background: #F0F0F0">
      <tr>
        <td align="center" valign="top" id="bodyCell">

          <table border="0" cellpadding="0" cellspacing="0" width="500" id="emailFooter">
            <tr>
              <td align="center" valign="top" style="background: #F0F0F0">
                <!-- CENTERING TABLE // -->
                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                  <tr>
                    <td align="center" valign="top">
                      <!-- FLEXIBLE CONTAINER // -->
                      <table border="0" cellpadding="0" cellspacing="0" width="500" class="">
                        <tr>
                          <td align="center" valign="top" width="500" class="flexibleContainerCell">
                            <table border="0" cellpadding="40" cellspacing="0" width="100%">
                              <tr>
                                <td valign="top"  style="padding: 25px;">

                                  <div style="font-size: 12px; color: #a3a3a3; text-align: center; font-family: inherit;">
                                    <div style="margin-bottom:8px;">Copyright &#169; %year <a target="_blank" href="https://platso.com" style="text-decoration:none;color:#a3a3a3;"><span style="color:#a3a3a3;">Platso</span></a> - All&nbsp;rights&nbsp;reserved.</div>
                                    <div><a target="_blank" href="https://www.platso.com/#/privacy" style="text-decoration:none !important;color:#a3a3a3;">Privacy Policy</a> - <a target="_blank" href="https://www.platso.com/#/terms-of-service" style="text-decoration:none !important;color:#a3a3a3;">Terms & Conditions</a> </div>
                                  </div>

                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                      <!-- // FLEXIBLE CONTAINER -->
                    </td>
                  </tr>
                </table>
                <!-- // CENTERING TABLE -->
              </td>
            </tr>

          </table>
          <!-- // END -->

        </td>
      </tr>
    </table>
  </center>
</body>
</html>
