import { Command as $Command } from "@smithy/smithy-client";
import { MetadataBearer as __MetadataBearer } from "@smithy/types";
import {
  CloudFormationClientResolvedConfig,
  ServiceInputTypes,
  ServiceOutputTypes,
} from "../CloudFormationClient";
import { DescribeEventsInput, DescribeEventsOutput } from "../models/models_0";
export { __MetadataBearer };
export { $Command };
export interface DescribeEventsCommandInput extends DescribeEventsInput {}
export interface DescribeEventsCommandOutput
  extends DescribeEventsOutput,
    __MetadataBearer {}
declare const DescribeEventsCommand_base: {
  new (
    input: DescribeEventsCommandInput
  ): import("@smithy/smithy-client").CommandImpl<
    DescribeEventsCommandInput,
    DescribeEventsCommandOutput,
    CloudFormationClientResolvedConfig,
    ServiceInputTypes,
    ServiceOutputTypes
  >;
  new (
    ...[input]: [] | [DescribeEventsCommandInput]
  ): import("@smithy/smithy-client").CommandImpl<
    DescribeEventsCommandInput,
    DescribeEventsCommandOutput,
    CloudFormationClientResolvedConfig,
    ServiceInputTypes,
    ServiceOutputTypes
  >;
  getEndpointParameterInstructions(): import("@smithy/middleware-endpoint").EndpointParameterInstructions;
};
export declare class DescribeEventsCommand extends DescribeEventsCommand_base {
  protected static __types: {
    api: {
      input: DescribeEventsInput;
      output: DescribeEventsOutput;
    };
    sdk: {
      input: DescribeEventsCommandInput;
      output: DescribeEventsCommandOutput;
    };
  };
}
