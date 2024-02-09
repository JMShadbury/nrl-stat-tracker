#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { RunnersStack } from '../lib/runners-stack';

const app = new cdk.App();


new RunnersStack(app, 'RunnersStack', {

});
