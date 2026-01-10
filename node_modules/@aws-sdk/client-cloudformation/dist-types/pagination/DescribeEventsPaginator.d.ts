import type { Paginator } from "@smithy/types";
import { DescribeEventsCommandInput, DescribeEventsCommandOutput } from "../commands/DescribeEventsCommand";
import { CloudFormationPaginationConfiguration } from "./Interfaces";
/**
 * @public
 */
export declare const paginateDescribeEvents: (config: CloudFormationPaginationConfiguration, input: DescribeEventsCommandInput, ...rest: any[]) => Paginator<DescribeEventsCommandOutput>;
