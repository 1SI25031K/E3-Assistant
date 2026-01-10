import { Command as $Command } from "@smithy/smithy-client";
import { MetadataBearer as __MetadataBearer } from "@smithy/types";
import {
  CloudFormationClientResolvedConfig,
  ServiceInputTypes,
  ServiceOutputTypes,
} from "../CloudFormationClient";
import { GetHookResultInput, GetHookResultOutput } from "../models/models_0";
export { __MetadataBearer };
export { $Command };
export interface GetHookResultCommandInput extends GetHookResultInput {}
export interface GetHookResultCommandOutput
  extends GetHookResultOutput,
    __MetadataBearer {}
declare const GetHookResultCommand_base: {
  new (
    input: GetHookResultCommandInput
  ): import("@smithy/smithy-client").CommandImpl<
    GetHookResultCommandInput,
    GetHookResultCommandOutput,
    CloudFormationClientResolvedConfig,
    ServiceInputTypes,
    ServiceOutputTypes
  >;
  new (
    ...[input]: [] | [GetHookResultCommandInput]
  ): import("@smithy/smithy-client").CommandImpl<
    GetHookResultCommandInput,
    GetHookResultCommandOutput,
    CloudFormationClientResolvedConfig,
    ServiceInputTypes,
    ServiceOutputTypes
  >;
  getEndpointParameterInstructions(): import("@smithy/middleware-endpoint").EndpointParameterInstructions;
};
export declare class GetHookResultCommand extends GetHookResultCommand_base {
  protected static __types: {
    api: {
      input: GetHookResultInput;
      output: GetHookResultOutput;
    };
    sdk: {
      input: GetHookResultCommandInput;
      output: GetHookResultCommandOutput;
    };
  };
}
