import { VerifySoftwareTokenResponseType } from "./enums";
import { CustomDomainConfigType, UserPoolClientType } from "./models_0";
export interface UpdateUserPoolClientResponse {
  UserPoolClient?: UserPoolClientType | undefined;
}
export interface UpdateUserPoolDomainRequest {
  Domain: string | undefined;
  UserPoolId: string | undefined;
  ManagedLoginVersion?: number | undefined;
  CustomDomainConfig?: CustomDomainConfigType | undefined;
}
export interface UpdateUserPoolDomainResponse {
  ManagedLoginVersion?: number | undefined;
  CloudFrontDomain?: string | undefined;
}
export interface VerifySoftwareTokenRequest {
  AccessToken?: string | undefined;
  Session?: string | undefined;
  UserCode: string | undefined;
  FriendlyDeviceName?: string | undefined;
}
export interface VerifySoftwareTokenResponse {
  Status?: VerifySoftwareTokenResponseType | undefined;
  Session?: string | undefined;
}
export interface VerifyUserAttributeRequest {
  AccessToken: string | undefined;
  AttributeName: string | undefined;
  Code: string | undefined;
}
export interface VerifyUserAttributeResponse {}
