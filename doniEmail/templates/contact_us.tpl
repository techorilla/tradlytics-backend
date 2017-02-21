<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
   <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Tempo-Responsive Email Template</title>

      <style type="text/css">
         /* Client-specific Styles */
         div, p, a, li, td { -webkit-text-size-adjust:none; }
         #outlook a {padding:0;} /* Force Outlook to provide a "view in browser" menu link. */
         html{width: 100%; }
         body{width:100% !important; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; margin:0; padding:0;}
         /* Prevent Webkit and Windows Mobile platforms from changing default font sizes, while not breaking desktop design. */
         .ExternalClass {width:100%;} /* Force Hotmail to display emails at full width */
         .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div {line-height: 100%;} /* Force Hotmail to display normal line spacing. */
         #backgroundTable {margin:0; padding:0; width:100% !important; line-height: 100% !important;}
         img {outline:none; text-decoration:none;border:none; -ms-interpolation-mode: bicubic;}
         a img {border:none;}
         .image_fix {display:block;}
         p {margin: 0px 0px !important;}
         table td {border-collapse: collapse;}
         table { border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; }
         a {color: #33b9ff;text-decoration: none;text-decoration:none!important;}
         /*STYLES*/
         table[class=full] { width: 100%; clear: both; }
         /*IPAD STYLES*/
         @media only screen and (max-width: 640px) {
         a[href^="tel"], a[href^="sms"] {
         text-decoration: none;
         color: #33b9ff; /* or whatever your want */
         pointer-events: none;
         cursor: default;
         }
         .mobile_link a[href^="tel"], .mobile_link a[href^="sms"] {
         text-decoration: default;
         color: #33b9ff !important;
         pointer-events: auto;
         cursor: default;
         }
         table[class=devicewidth] {width: 440px!important;text-align:center!important;}
         table[class=devicewidthinner] {width: 420px!important;text-align:center!important;}
         img[class=banner] {width: 440px!important;height:220px!important;}
         img[class=col2img] {width: 440px!important;height:220px!important;}


         }
         /*IPHONE STYLES*/
         @media only screen and (max-width: 480px) {
         a[href^="tel"], a[href^="sms"] {
         text-decoration: none;
         color: #33b9ff; /* or whatever your want */
         pointer-events: none;
         cursor: default;
         }
         .mobile_link a[href^="tel"], .mobile_link a[href^="sms"] {
         text-decoration: default;
         color: #33b9ff !important;
         pointer-events: auto;
         cursor: default;
         }
         table[class=devicewidth] {width: 280px!important;text-align:center!important;}
         table[class=devicewidthinner] {width: 260px!important;text-align:center!important;}
         img[class=banner] {width: 280px!important;height:140px!important;}
         img[class=col2img] {width: 280px!important;height:140px!important;}


         }
      </style>
   </head>
   <body>
<!-- Start of preheader -->
<!-- <table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="preheader" >
   <tbody>
      <tr>
         <td>
            <table width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody>
                  <tr>
                     <td width="100%">
                        <table width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
                           <tbody> -->
                              <!-- Spacing -->
                             <!--  <tr>
                                 <td width="100%" height="20"></td>
                              </tr> -->
                              <!-- Spacing -->
                              <!-- <tr>
                                 <td width="100%" align="left" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 13px;color: #282828" st-content="preheader">
                                    Can't see this Email? View it in your <a href="#" style="text-decoration: none; color: #eacb3c">Browser </a>
                                 </td>
                              </tr> -->
                              <!-- Spacing -->
                              <!-- <tr>
                                 <td width="100%" height="20"></td>
                              </tr> -->
                              <!-- Spacing -->
                           <!-- </tbody>
                        </table>
                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table> -->
<!-- End of preheader -->
<!-- Start of seperator -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="seperator">
   <tbody>
      <tr>
         <td>
            <table width="800" align="center" cellspacing="0" cellpadding="0" border="0" class="devicewidth">
               <tbody>
                  <tr>
                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of seperator -->
<!-- Start of header -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="header">
   <tbody>
      <tr>
         <td>
            <table width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody>
                  <tr>
                     <td width="100%">
                        <table width="800" bgcolor="#eacb3c" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
                           <tbody>
                              <tr>
                                 <td>
                                    <!-- logo -->
                                    <table bgcolor="#fff" width="800" align="left" border="0" cellpadding="0" cellspacing="0" class="devicewidth">
                                       <tbody>
                                          <tr>
                                             <td width="140" height="50" align="center">
                                                <div class="imgpop">
                                                   <a target="_blank" href="https://donigroup.com">
                                                   <img src="cid:logo.png" alt="" border="0" width="180" height="100" style="display:block; border:none; outline:none; text-decoration:none; padding-bottom:10px; padding-top:10px;">
                                                   </a>
                                                </div>
                                             </td>
                                          </tr>
                                       </tbody>
                                    </table>
                                    <!-- end of logo -->
                                    <!-- start of menu -->
                                    <!-- <table bgcolor="#eacb3c" width="250" height="50" border="0" align="right" valign="middle" cellpadding="0" cellspacing="0" border="0" class="devicewidth">
                                       <tbody>
                                          <tr>
                                             <td height="50" align="center" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 13px;color: #282828" st-content="menu">
                                                <a href="#" style="color: #282828;text-decoration: none;">Home</a>
                                                &nbsp;&nbsp;&nbsp;
                                                <a href="#" style="color: #282828;text-decoration: none;">Shop</a>
                                                &nbsp;&nbsp;&nbsp;
                                                <a href="#" style="color: #282828;text-decoration: none;">Contact</a>
                                                &nbsp;&nbsp;&nbsp;
                                             </td>
                                          </tr>
                                       </tbody>
                                    </table> -->
                                    <!-- end of menu -->
                                 </td>
                              </tr>
                           </tbody>
                        </table>
                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of Header -->

<!-- Start of main-banner -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="banner">
   <tbody>
      <tr>
         <td>
            <table width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody>
                  <tr>
                     <td width="100%">
                        <table width="800" align="center" cellspacing="0" cellpadding="0" border="0" class="devicewidth">
                           <tbody>
                              <tr>
                                 <!-- start of image -->
                                 <td align="center" st-image="banner-image">
                                    <div class="imgpop">
                                       <a target="_blank" href="#"><img width="800" border="0" height="250" alt="" border="0" style="display:block; border:none; outline:none; text-decoration:none;" src="cid:blog-background.jpg" class="banner"></a>
                                    </div>
                                 </td>
                              </tr>
                           </tbody>
                        </table>
                        <!-- end of image -->
                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of main-banner -->
<!-- Start of seperator -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="seperator">
   <tbody>
      <tr>
         <td>
            <table bgcolor="#ffffff" width="800" align="center" cellspacing="0" cellpadding="0" border="0" class="devicewidth">
               <tbody>
                  <tr>
                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of seperator -->
<!-- Start of Left Image -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="left-image">
   <tbody>
      <tr>
         <td>
            <table width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody style="background: #fff;">
                  <tr>
                     <td width="100%">
                        <table width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
                           <tbody>
                              <tr>
                                 <td>
                                    <!-- end of left column -->
                                    <!-- spacing for mobile devices-->
                                    <table align="left" border="0" cellpadding="0" cellspacing="0" class="mobilespacing">
                                       <tbody>
                                          <tr>
                                             <td width="100%" height="15" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                                          </tr>
                                       </tbody>
                                    </table>
                                    <!-- end of for mobile devices-->
                                    <!-- start of right column -->
                                    <table width="700" align="right" border="0" cellpadding="0" cellspacing="0" class="devicewidth">
                                       <tbody>
                                          <tr>
                                             <td>
                                                <table width="700" align="center" border="0" cellpadding="0" cellspacing="0" class="devicewidth">
                                                   <tbody>
                                                      <!-- title -->
                                                      <tr>
                                                         <td style="font-family: Helvetica, arial, sans-serif; font-size: 18px; color: #282828; text-align:left; line-height: 24px;">
                                                            Greetings %name! Thanks for contacting us
                                                         </td>
                                                      </tr>
                                                      <!-- end of title -->
                                                      <!-- Spacing -->
                                                      <tr>
                                                         <td width="100%" height="15" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                                                      </tr>
                                                      <!-- /Spacing -->
                                                      <!-- content -->
                                                      <tr>
                                                         <td style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #889098; text-align:left; line-height: 24px; padding-right:50px;">
                                                            Doni & Company is international commodity brokerage firm in business since last 30 years, Our market research based on decades of trading data has helped us make wiser decisions for our clients. We track your transcations on each step and focus on optimizing your trade revenues.
                                                         </td>


                                                      </tr>

                                                      <tr>
                                                         <td style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #889098; text-align:left; line-height: 24px;  padding-right:50px; padding-top:10px;">
                                                            We would be happy to work with you and help you make better decisions maximizing your trade revenues. One of our representatives will contact you shortly. Till then click on the button below to check our products, daily prices and market analysis.
                                                         </td>


                                                      </tr>


                                                      <!-- end of content -->
                                                      <!-- Spacing -->
                                                      <tr>
                                                         <td width="100%" height="15" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                                                      </tr>
                                                      <!-- /Spacing -->
                                                      <!-- read more -->
                                                      <tr>
                                                         <td>
                                                            <table width="220" height="32" bgcolor="#eacb3c" align="left" valign="middle" border="0" cellpadding="0" cellspacing="0" style="border-radius:3px;" st-button="learnmore">
                                                               <tbody>
                                                                  <tr>
                                                                     <td height="9" align="center" style="font-size:1px; line-height:1px;">&nbsp;</td>
                                                                  </tr>
                                                                  <tr>
                                                                     <td height="14" align="center" valign="middle" style="font-family: Helvetica, Arial, sans-serif; font-size: 13px; font-weight:bold;color: #ffffff; text-align:center; line-height: 14px; ; -webkit-text-size-adjust:none;" st-title="fulltext-btn">
                                                                        <a style="text-decoration: none;color: #282828; text-align:center;" href="http://tramodity.com/products.html">Doni and Company Products</a>
                                                                     </td>
                                                                  </tr>
                                                                  <tr>
                                                                     <td height="9" align="center" style="font-size:1px; line-height:1px;">&nbsp;</td>
                                                                  </tr>
                                                               </tbody>
                                                            </table>
                                                         </td>
                                                      </tr>

                                                      <tr>
                                                         <td style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #000; text-align:left; line-height: 24px;  padding-right:50px; padding-top:10px; font-weight:bold;">
                                                            Looking forward to work with you.
                                                         </td>
                                                      </tr>

                                                      <tr>
                                                         <td style="font-family: Helvetica, arial, sans-serif; font-size: 14px; color: #000000; text-align:left; line-height: 15px;  padding-right:50px; padding-top:10px;  font-weight:bold;">
                                                            Arif Doni <br>
                                                         </td>
                                                      </tr>

                                                      <tr>
                                                         <td style="font-family: Helvetica, arial, sans-serif; font-size: 12px; color: #889098; text-align:left; line-height: 15px;  padding-right:50px;">
                                                            <p style="font-size:12px">CEO</p> <p style="font-size:12px">Doni & Company</p>
                                                         </td>
                                                      </tr>
                                                      <!-- end of read more -->
                                                   </tbody>
                                                </table>
                                             </td>
                                          </tr>
                                       </tbody>
                                    </table>
                                    <!-- end of right column -->
                                 </td>
                              </tr>
                           </tbody>
                        </table>
                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of Left Image -->
<!-- Start of seperator -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="seperator">
   <tbody>
      <tr>
         <td>
            <table  bgcolor="#fff" width="800" align="center" cellspacing="0" cellpadding="0" border="0" class="devicewidth">
               <tbody>
                  <tr>
                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of seperator -->
<!-- Start of seperator -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="seperator">
   <tbody>
      <tr>
         <td>
            <table bgcolor="#fff" width="800" align="center" cellspacing="0" cellpadding="0" border="0" class="devicewidth">
               <tbody>
                  <tr>
                     <td align="center" height="30" style="font-size:1px; line-height:1px;">&nbsp;</td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of seperator -->

<!-- Start of footer -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="footer">
   <tbody>
      <tr>
         <td>
            <table width="800" bgcolor="#3D3938" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody>
                  <tr>
                     <td width="100%">
                        <table bgcolor="#3D3938" width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
                           <tbody>
                              <!-- Spacing -->
                              <tr>
                                 <td height="10" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                              </tr>
                              <!-- Spacing -->
                              <tr>
                                 <td>
                                    <table width="800" align="center" border="0" cellpadding="0" cellspacing="0" class="devicewidth">
                                       <tbody>
                                          <tr>
                                             <td align="center" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 13px;color: #889094" st-content="preheader">
                        101, Shalimar Centre, Altaf Hussain Road </td>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 12px; color: #889094; text-align:center; line-height: 15px;">
                                             </td>
                                          </tr>

                                          <tr>
                                             <td align="center" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 13px;color: #889094" st-content="preheader">
                        New Challi, Karachi, Pakistan 74200  </td>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 12px; color: #889094; text-align:center; line-height: 15px;">
                                             </td>
                                          </tr>

                                          <tr>
                                             <td align="center" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 13px;color: #889094" st-content="preheader">
                        New (92)-21-32430152-5 (4 Lines)    </td>
                                             <td style="font-family: Helvetica, arial, sans-serif; font-size: 12px; color: #889094; text-align:center; line-height: 15px;">
                                             </td>
                                          </tr>

                                       </tbody>
                                    </table>
                                    <!-- Social icons -->
                                    <table  width="150" align="center" border="0" cellpadding="0" cellspacing="0" class="devicewidth" style="margin-top:10px">
                                       <tbody>
                                          <tr>
                                             <td width="23" height="23" align="center">
                                                <div class="imgpop">
                                                   <a target="_blank" href="https://www.facebook.com/DoniGroup/">
                                                   <img src="cid:facebook.png" alt="" border="0" width="23" height="23" style="display:block; border:none; outline:none; text-decoration:none;">
                                                   </a>
                                                </div>
                                             </td>
                                             <td align="left" width="5" style="font-size:1px; line-height:1px;">&nbsp;</td>
                                             <td width="23" height="23" align="center">
                                                <div class="imgpop">
                                                   <a target="_blank" href="https://twitter.com/DoniCompany">
                                                   <img src="cid:twitter.png" alt="" border="0" width="23" height="23" style="display:block; border:none; outline:none; text-decoration:none;">
                                                   </a>
                                                </div>
                                             </td>
                                             <td align="left" width="5" style="font-size:1px; line-height:1px;">&nbsp;</td>
                                             <td width="23" height="23" align="center">
                                                <div class="imgpop">
                                                   <a target="_blank" href="https://www.linkedin.com/company/doni-and-company">
                                                   <img src="cid:linkedin.png" alt="" border="0" width="23" height="23" style="display:block; border:none; outline:none; text-decoration:none;">
                                                   </a>
                                                </div>
                                             </td>
                                          </tr>
                                       </tbody>
                                    </table>
                                    <!-- end of Social icons -->
                                 </td>
                              </tr>
                              <!-- Spacing -->
                              <tr>
                                 <td height="10" style="font-size:1px; line-height:1px; mso-line-height-rule: exactly;">&nbsp;</td>
                              </tr>
                              <!-- Spacing -->
                           </tbody>
                        </table>
                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
<!-- End of footer -->
<!-- Start of Postfooter -->
<table width="100%" bgcolor="#545555" cellpadding="0" cellspacing="0" border="0" id="backgroundTable" st-sortable="postfooter" >
   <tbody>
      <tr>
         <td>
            <table width="800" cellpadding="0" cellspacing="0" border="0" align="center" class="devicewidth">
               <tbody>
                  <!-- Spacing -->
                  <tr>
                     <td width="100%" height="20"></td>
                  </tr>
                  <!-- Spacing -->
                  <tr>
                     <td align="center" valign="middle" style="font-family: Helvetica, arial, sans-serif; font-size: 13px;color: #282828" st-content="preheader">
                        Copyright © %year.<a href="#" style="text-decoration: none; color: #889094">Doni & Company</a>
                     </td>
                  </tr>
                  <!-- Spacing -->
                  <tr>
                     <td width="100%" height="20"></td>
                  </tr>
                  <!-- Spacing -->
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
<!-- <!-- </table>  -->
<!-- End of postfooter  -->
   </body>
   </html>