import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Location, LocationDocument } from './schema/location.schema';
import { CreateLocationDto } from './dto/create-location.dto';
import { UpdateLocationDto } from './dto/update-location.dto';

@Injectable()
export class LocationService {
  constructor(
    @InjectModel(Location.name) private locationModel: Model<LocationDocument>,
  ) {}

  async create(createLocationDto: CreateLocationDto): Promise<Location> {
    const newLocation = new this.locationModel(createLocationDto);
    console.log("create a location")
    return newLocation.save();
  }

  async findAll(): Promise<Location[] | { message: string }>  {
    const locations = await this.locationModel.find();

  if (locations.length === 0) {
    return { message: 'No locations found' };
  }

    return locations;
  }

  async findOne(id: string): Promise<Location> {
    const location = await this.locationModel.findById(id);
    if (!location) {
      throw new NotFoundException(`Location #${id} not found`);
    }

    console.log(`FindID ${id}`)
    return location;
  }

  async update(id: string, updateLocationDto: UpdateLocationDto): Promise<Location> {
    const updatedLocation = await this.locationModel.findByIdAndUpdate(
      id,
      updateLocationDto,
      { new: true },
    );

    if (!updatedLocation) {
      throw new NotFoundException(`Location #${id} not found`);
    }
    console.log(`update Patch ${id}`)

    return updatedLocation;
  }

  async remove(id: string): Promise<{ message: string }> {
    const result = await this.locationModel.findByIdAndDelete(id);
    if (!result) {
      throw new NotFoundException(`Location #${id} not found`);
    }
    console.log(`remove location ${id}`)
    return { message: `Location #${id} removed successfully` };
  }
}