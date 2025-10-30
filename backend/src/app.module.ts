import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';

import { MongooseModule } from '@nestjs/mongoose';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { HealthcareModule } from './healthcare/healthcare.module';
import { LocationModule } from './location/location.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
    }),
    MongooseModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: async (configService: ConfigService) => {
        const mongodb_user = configService.get<string>('mongodb_user');
        const mongodb_password = configService.get<string>('mongodb_password');

        // const URL = `mongodb+srv://${mongodb_user}:${mongodb_password}@freecluster.fmh5ckt.mongodb.net/?appName=freecluster` //default 
        const URL = `mongodb+srv://${mongodb_user}:${mongodb_password}@freecluster.fmh5ckt.mongodb.net/main?retryWrites=true&w=majority`
        // console.log(URL)

        return {
          uri: URL,
          useNewUrlParser: true,
          useUnifiedTopology: true,
        };
      },
    }),
    LocationModule, 
    HealthcareModule
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

