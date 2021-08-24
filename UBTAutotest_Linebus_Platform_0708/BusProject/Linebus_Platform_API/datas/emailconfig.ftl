<!DOCTYPE html>
<html lang="en">
<meta name="renderer" content="webkit">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="format-detection" content="telephone=no,email=no,adress=no" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" />
<head>
  <meta charset="UTF-8">
  <title>Document</title>
</head>
<body>
    <style>
        .mainColor{
            color:#FF1C00
        }
    </style>
    <div style="font: 14px/24px Tahoma, Verdana, Arial, sans-serif;">
        <div style="margin: 30px auto 0px; max-width: 650px; text-align:justify;line-height:0;">
            <div style="display:inline-block; vertical-align: middle; padding:10px 0">
                <img style="max-width:180px; max-height:70px;" class="logoimg" src="${mailLogo}">
            </div>
            <div style="display:inline-block; vertical-align: bottom; line-height:30px; padding:10px 0 15px">
                <img style=" vertical-align: middle; " src="${mailPhoneIcon}">
                <span style=" font-size: 24px; height:30px; vertical-align: middle; display: inline-block; font-family: impact;letter-spacing: 1px;font-style: italic;">${mailPhone!}</span>
            </div>
            <div style="display:inline-block; height: 0; line-height: 0; width:100%;"></div>
        </div>
        <div style="margin: 0 auto; max-width: 650px">
            <div style=" overflow:hidden; padding: 15px 20px; border: 1px solid #eee;">
                <p>Dear ${ContactName!},</p>

                <p>Here's the link you need to sign our Youth Travel Alone Agreement. It should be filled out by the non-travelling parents/guardians.</p>
				<p style="text-align:center;"></p>
				<div style=" text-align:center;">
                    <div style="padding:10px 20px; border:1px dashed #aaa; background:#fafafa; display: inline-block; border-radius: 5px; font-size:16px;font-weight: bold;">
						<a href=${agreementOnlineUrl!} >Click to Sign</a>
					</div>
                </div>
                <p style="color:#888; font-size: 12px; margin-top:30px; text-align:right;">The ${mailCompanyName!} Team</p>
                <p style="color:#888; font-size: 12px; margin-top:30px; text-align:right;"><a href=${website!}>${website!}</a></p>
            </div>
        </div>
        <div style="margin: 0 auto; max-width: 650px; text-align:center; font-size:12px;background:#eee;padding:10px 0; line-height:12px; color:#666;">Copyright © ${mailCopyrightYear!} <span>${mailCompanyName!}</span>. All Rights Reserved.</div>
    </div>
</body>
</html>