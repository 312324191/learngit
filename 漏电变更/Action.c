Action()
{
    lr_output_message("timestamp1 = %s", lr_eval_string("{timestamp1}")); 
    lr_output_message("svc_number = %s", lr_eval_string("{svc_number}")); 
    web_reg_find("Text=SUCCESS",
 		LAST);
   	lr_start_transaction("ldbg");

	web_custom_request("url",

		"URL=https://10.124.5.208:8006/OSN/vop/basic_service/modify_service_lsms/v6?token=hcOPBgJ4dB8WBy1V5nrpGaIqaP2INnrhRd0IZ4GflgtCPWsY",
		"Method=POST",
		"RecContentType=application/json;charset=UTF-8",

		"TargetFrame=",
		"Resource=0",
		"Referer=",
        "Mode=HTTP",
		"EncType=application/json;charset=UTF-8",
		"Body={"
 "       \"api_name\": \"cu.vop.basic_service.modify_service_lsms\", "
 "       \"mvnokey\": \"OJvWpmI\", "
 "       \"serial_number\": \"{random4}{timestamp1}{random4}{random4}{random4}\", "
 "       \"timestamp\": \"{timestamp}\"," 
 "       \"service_type\": \"basic_service\", "
 "       \"service_name\": \"modify_service_lsms\", "

  "      \"data\": {"
 "          \"order_id\": \"{random4}{timestamp1}{random4}{random4}{random4}{random4}\", "
 "           \"phone_number\": {svc_number}"
          
 "       }"
"    }",
		LAST);


	lr_end_transaction("ldbg", LR_AUTO);

	return 0;
}
