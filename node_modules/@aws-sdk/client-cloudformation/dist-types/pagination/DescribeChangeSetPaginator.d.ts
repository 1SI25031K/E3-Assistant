import type { Paginator } from "@smithy/types";
import { DescribeChangeSetCommandInput, DescribeChangeSetCommandOutput } from "../commands/DescribeChangeSetCommand";
import { CloudFormationPaginationConfiguration } from "./Interfaces";
/**
 * @public
 */
export declare const paginateDescribeChangeSet: (config: CloudFormationPaginationConfiguration, input: DescribeChangeSetCommandInput, ...rest: any[]) => Paginator<DescribeChangeSetCommandOutput>;
