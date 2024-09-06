import { effect, Injectable, signal } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ThemeService {
  selectedTheme!:string;
  themeSignal = signal<string>( 
    JSON.parse(localStorage.getItem('theme') ?? '"light"')
  );

  constructor() {
    effect(() => {
      localStorage.setItem('theme', JSON.stringify(this.themeSignal()));
    });
   }

  setTheme(theme:string):void {
    this.themeSignal.set(theme)
  }

  updateTheme():void{
    this.themeSignal.update(value =>(value === "light"?"dark":"light"));
    this.selectedTheme = this.themeSignal();
    
  }

}
